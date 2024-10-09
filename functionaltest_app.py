# test_functional.py
import unittest
import json
from app import app, db, Guepardo

class TestGuepardoAPIFunctional(unittest.TestCase):
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

    # Prueba funcional completa: Crear, leer, actualizar y eliminar un guepardo
    def test_funcionalidad_completa_crud(self):
        # 1. Crear un nuevo guepardo
        datos_guepardo = {
            "nombre": "Guepardo Funcional",
            "edad": 3,
            "velocidad_maxima": 100.0,
            "habitat": "Sabana"
        }
        response = self.app.post('/guepardos', data=json.dumps(datos_guepardo), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Verificar que el guepardo se haya creado correctamente
        data_creado = json.loads(response.data)
        guepardo_id = data_creado['guepardo']['id']
        self.assertEqual(data_creado['guepardo']['nombre'], "Guepardo Funcional")
        self.assertEqual(data_creado['guepardo']['edad'], 3)

        # 2. Obtener todos los guepardos y verificar que el guepardo recién creado esté presente
        response = self.app.get('/guepardos')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], "Guepardo Funcional")

        # 3. Obtener el guepardo creado por ID
        response = self.app.get(f'/guepardos/{guepardo_id}')
        self.assertEqual(response.status_code, 200)
        guepardo = json.loads(response.data)
        self.assertEqual(guepardo['nombre'], "Guepardo Funcional")
        self.assertEqual(guepardo['velocidad_maxima'], 100.0)

        # 4. Actualizar los datos del guepardo
        nuevos_datos = {
            "nombre": "Guepardo Actualizado",
            "edad": 4,
            "velocidad_maxima": 110.0,
            "habitat": "Bosque"
        }
        response = self.app.put(f'/guepardos/{guepardo_id}', data=json.dumps(nuevos_datos), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Verificar que los datos se hayan actualizado correctamente
        data_actualizado = json.loads(response.data)
        self.assertEqual(data_actualizado['guepardo']['nombre'], "Guepardo Actualizado")
        self.assertEqual(data_actualizado['guepardo']['edad'], 4)
        self.assertEqual(data_actualizado['guepardo']['velocidad_maxima'], 110.0)

        # 5. Eliminar el guepardo
        response = self.app.delete(f'/guepardos/{guepardo_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Guepardo eliminado exitosamente", response.get_data(as_text=True))

        # Verificar que el guepardo ha sido eliminado
        response = self.app.get(f'/guepardos/{guepardo_id}')
        self.assertEqual(response.status_code, 404)

    # Prueba funcional: Verificación de manejo de errores (datos incompletos)
    def test_manejo_de_errores_creacion_incompleta(self):
        # Intentamos crear un guepardo sin algunos datos requeridos
        datos_incompletos = {
            "nombre": "Guepardo Erroneo",
            "edad": 3
            # Falta velocidad_maxima y habitat
        }
        response = self.app.post('/guepardos', data=json.dumps(datos_incompletos), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Datos incompletos", response.get_data(as_text=True))

    # Prueba funcional: Verificar si se obtienen los datos correctamente después de múltiples operaciones
    def test_varias_operaciones_seguidas(self):
        # Crear varios guepardos
        guepardos = [
            {"nombre": "Guepardo 1", "edad": 2, "velocidad_maxima": 95.0, "habitat": "Desierto"},
            {"nombre": "Guepardo 2", "edad": 4, "velocidad_maxima": 110.0, "habitat": "Sabana"},
            {"nombre": "Guepardo 3", "edad": 5, "velocidad_maxima": 115.0, "habitat": "Montaña"}
        ]
        for guepardo in guepardos:
            response = self.app.post('/guepardos', data=json.dumps(guepardo), content_type='application/json')
            self.assertEqual(response.status_code, 201)

        # Verificar que se hayan creado todos
        response = self.app.get('/guepardos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['nombre'], "Guepardo 1")
        self.assertEqual(data[1]['nombre'], "Guepardo 2")
        self.assertEqual(data[2]['nombre'], "Guepardo 3")

    # Prueba funcional: Verificación de un ID que no existe
    def test_obtener_guepardo_inexistente(self):
        # Intentamos obtener un guepardo que no existe
        response = self.app.get('/guepardos/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Guepardo no encontrado", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
