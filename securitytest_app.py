# test_security.py
import unittest
import json
from app import app, db, Guepardo

class TestGuepardoAPISecurity(unittest.TestCase):
    def setUp(self):
        # Configuración inicial de la aplicación en modo de prueba
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usamos una base de datos en memoria
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Eliminamos la sesión y las tablas después de cada prueba
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Prueba de inyección SQL
    def test_inyeccion_sql(self):
        # Intentar inyección SQL en la creación de un nuevo guepardo
        datos_maliciosos = {
            "nombre": "'; DROP TABLE guepardo; --",
            "edad": 3,
            "velocidad_maxima": 100.0,
            "habitat": "Sabana"
        }
        response = self.app.post('/guepardos', data=json.dumps(datos_maliciosos), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Datos incompletos", response.get_data(as_text=True))  # Validamos que la app no acepte inyección SQL

        # Verificar que la tabla 'guepardo' no se haya eliminado
        response = self.app.get('/guepardos')
        self.assertEqual(response.status_code, 200)

    # Prueba de inyección SQL en el parámetro de consulta
    def test_inyeccion_sql_en_parametro(self):
        # Intentamos una inyección SQL en la ruta de obtención de un guepardo por ID
        response = self.app.get("/guepardos/1 OR 1=1")
        self.assertEqual(response.status_code, 404)  # La aplicación no debería ser vulnerable a inyecciones SQL

    # Prueba de XSS (Cross-Site Scripting)
    def test_xss_en_nombre(self):
        # Intentamos inyectar un script malicioso en el campo 'nombre'
        datos_xss = {
            "nombre": "<script>alert('xss');</script>",
            "edad": 4,
            "velocidad_maxima": 110.0,
            "habitat": "Sabana"
        }
        response = self.app.post('/guepardos', data=json.dumps(datos_xss), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Verificar que el nombre se haya guardado sin ejecutar el script
        guepardo_creado = json.loads(response.data)
        self.assertNotIn("<script>", guepardo_creado['guepardo']['nombre'])  # No debe permitir etiquetas HTML

    # Prueba de acceso indebido a un ID no existente (Evitar revelación de información)
    def test_acceso_invalido_a_id(self):
        # Intentamos acceder a un guepardo con un ID no existente
        response = self.app.get('/guepardos/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Guepardo no encontrado", response.get_data(as_text=True))

    # Prueba de longitud excesiva de campos
    def test_longitud_excesiva_de_campos(self):
        # Intentar enviar datos extremadamente largos para probar si la aplicación lo maneja correctamente
        datos_largos = {
            "nombre": "A" * 10000,  # Nombre con 10,000 caracteres
            "edad": 5,
            "velocidad_maxima": 110.0,
            "habitat": "B" * 10000  # Habitat con 10,000 caracteres
        }
        response = self.app.post('/guepardos', data=json.dumps(datos_largos), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Esperamos un error por longitud de datos

    # Prueba de validación de tipo de datos (prevención de tipo de datos maliciosos)
    def test_validacion_de_tipo_de_datos(self):
        # Intentamos enviar una edad no válida (un string en lugar de un entero)
        datos_invalidos = {
            "nombre": "Guepardo Invalido",
            "edad": "tres",  # Esto debería causar un error
            "velocidad_maxima": 110.0,
            "habitat": "Sabana"
        }
        response = self.app.post('/guepardos', data=json.dumps(datos_invalidos), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Datos incompletos", response.get_data(as_text=True))  # El error de validación debería aparecer

if __name__ == '__main__':
    unittest.main()
