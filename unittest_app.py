# test_app.py
import unittest
import json
from app import app, db, Guepardo

class TestGuepardoAPI(unittest.TestCase):
    def setUp(self):
        # Configurar la aplicación en modo de prueba
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        # Eliminar la sesión y las tablas después de cada prueba
        db.session.remove()
        db.drop_all()

    def test_crear_guepardo(self):
        # Probar la creación de un guepardo
        datos_guepardo = {
            "nombre": "Guepardo de Prueba",
            "edad": 5,
            "velocidad_maxima": 110.0,
            "habitat": "Sabana"
        }
        response = self.app.post('/guepardos', data=json.dumps(datos_guepardo), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("Guepardo creado exitosamente", response.get_data(as_text=True))

    def test_obtener_guepardos(self):
        # Probar la obtención de todos los guepardos
        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo A",
            "edad": 4,
            "velocidad_maxima": 120.0,
            "habitat": "Bosque"
        }), content_type='application/json')

        response = self.app.get('/guepardos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], "Guepardo A")

    def test_obtener_guepardo_por_id(self):
        # Probar la obtención de un guepardo por ID
        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo B",
            "edad": 3,
            "velocidad_maxima": 130.0,
            "habitat": "Desierto"
        }), content_type='application/json')

        response = self.app.get('/guepardos/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], "Guepardo B")

    def test_actualizar_guepardo(self):
        # Probar la actualización de un guepardo
        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo C",
            "edad": 6,
            "velocidad_maxima": 115.0,
            "habitat": "Montaña"
        }), content_type='application/json')

        actualizar_datos = {
            "nombre": "Guepardo C Actualizado",
            "velocidad_maxima": 125.0
        }
        response = self.app.put('/guepardos/1', data=json.dumps(actualizar_datos), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['guepardo']['nombre'], "Guepardo C Actualizado")
        self.assertEqual(data['guepardo']['velocidad_maxima'], 125.0)

    def test_eliminar_guepardo(self):
        # Probar la eliminación de un guepardo
        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo D",
            "edad": 7,
            "velocidad_maxima": 130.0,
            "habitat": "Llanura"
        }), content_type='application/json')

        response = self.app.delete('/guepardos/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Guepardo eliminado exitosamente", response.get_data(as_text=True))

        # Verificar que ya no existe
        response = self.app.get('/guepardos/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
