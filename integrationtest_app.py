# test_integration.py
import unittest
import json
from app import app, db, Guepardo

class TestGuepardoAPIIntegration(unittest.TestCase):
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

    # Prueba de integración para la creación de un guepardo (POST)
    def test_crear_guepardo(self):
        datos_guepardo = {
            "nombre": "Guepardo de Prueba",
            "edad": 5,
            "velocidad_maxima": 110.0,
            "habitat": "Sabana"
        }
        response = self.app.post('/guepardos', data=json.dumps(datos_guepardo), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("Guepardo creado exitosamente", response.get_data(as_text=True))

        # Verificar que el guepardo se haya creado en la base de datos
        guepardos = Guepardo.query.all()
        self.assertEqual(len(guepardos), 1)
        self.assertEqual(guepardos[0].nombre, "Guepardo de Prueba")

    # Prueba de integración para obtener todos los guepardos (GET)
    def test_obtener_todos_los_guepardos(self):
        # Crear algunos guepardos de prueba
        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo A",
            "edad": 4,
            "velocidad_maxima": 120.0,
            "habitat": "Bosque"
        }), content_type='application/json')

        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo B",
            "edad": 6,
            "velocidad_maxima": 125.0,
            "habitat": "Montaña"
        }), content_type='application/json')

        # Hacer una solicitud GET para obtener todos los guepardos
        response = self.app.get('/guepardos')
        self.assertEqual(response.status_code, 200)

        # Verificar que se obtuvieron los guepardos correctamente
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['nombre'], "Guepardo A")
        self.assertEqual(data[1]['nombre'], "Guepardo B")

    # Prueba de integración para obtener un guepardo por ID (GET)
    def test_obtener_guepardo_por_id(self):
        # Crear un guepardo de prueba
        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo C",
            "edad": 3,
            "velocidad_maxima": 130.0,
            "habitat": "Desierto"
        }), content_type='application/json')

        # Hacer una solicitud GET para obtener el guepardo por ID
        response = self.app.get('/guepardos/1')
        self.assertEqual(response.status_code, 200)

        # Verificar los datos del guepardo obtenido
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], "Guepardo C")
        self.assertEqual(data['velocidad_maxima'], 130.0)

    # Prueba de integración para actualizar un guepardo por ID (PUT)
    def test_actualizar_guepardo(self):
        # Crear un guepardo de prueba
        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo D",
            "edad": 6,
            "velocidad_maxima": 115.0,
            "habitat": "Sabana"
        }), content_type='application/json')

        # Actualizar el guepardo con nuevos datos
        datos_actualizados = {
            "nombre": "Guepardo D Actualizado",
            "velocidad_maxima": 125.0
        }
        response = self.app.put('/guepardos/1', data=json.dumps(datos_actualizados), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Verificar que los datos fueron actualizados en la base de datos
        guepardo_actualizado = Guepardo.query.get(1)
        self.assertEqual(guepardo_actualizado.nombre, "Guepardo D Actualizado")
        self.assertEqual(guepardo_actualizado.velocidad_maxima, 125.0)

    # Prueba de integración para eliminar un guepardo por ID (DELETE)
    def test_eliminar_guepardo(self):
        # Crear un guepardo de prueba
        self.app.post('/guepardos', data=json.dumps({
            "nombre": "Guepardo E",
            "edad": 7,
            "velocidad_maxima": 130.0,
            "habitat": "Llanura"
        }), content_type='application/json')

        # Eliminar el guepardo por ID
        response = self.app.delete('/guepardos/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Guepardo eliminado exitosamente", response.get_data(as_text=True))

        # Verificar que el guepardo fue eliminado de la base de datos
        guepardos = Guepardo.query.all()
        self.assertEqual(len(guepardos), 0)

    # Prueba de integración para errores (Por ejemplo, obtener un guepardo que no existe)
    def test_error_guepardo_no_encontrado(self):
        # Intentar obtener un guepardo que no existe
        response = self.app.get('/guepardos/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Guepardo no encontrado", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
