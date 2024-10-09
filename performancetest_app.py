# test_performance.py
import unittest
import json
from app import app, db, Guepardo
import pytest

class TestGuepardoAPIPerformance(unittest.TestCase):
    def setUp(self):
        # Configuración inicial de la aplicación en modo de prueba
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usamos una base de datos en memoria para pruebas
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Eliminamos la sesión y las tablas después de cada prueba
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Prueba de rendimiento para crear guepardos
    @pytest.mark.benchmark
    def test_crear_guepardo_benchmark(self, benchmark):
        def crear_guepardo():
            datos = {
                "nombre": "Guepardo Veloz",
                "edad": 4,
                "velocidad_maxima": 120.5,
                "habitat": "Sabana Africana"
            }
            response = self.app.post('/guepardos', data=json.dumps(datos), content_type='application/json')
            return response

        # Medimos el rendimiento
        result = benchmark(crear_guepardo)
        assert result.status_code == 201

    # Prueba de rendimiento para obtener todos los guepardos
    @pytest.mark.benchmark
    def test_obtener_guepardos_benchmark(self, benchmark):
        # Primero agregamos varios guepardos
        for i in range(100):
            nuevo_guepardo = Guepardo(nombre=f"Guepardo {i}", edad=5, velocidad_maxima=100.0, habitat="Sabana")
            with app.app_context():
                db.session.add(nuevo_guepardo)
                db.session.commit()

        # Benchmarking para obtener todos los guepardos
        def obtener_guepardos():
            return self.app.get('/guepardos')

        # Medimos el rendimiento
        result = benchmark(obtener_guepardos)
        assert result.status_code == 200

    # Prueba de rendimiento para actualizar un guepardo
    @pytest.mark.benchmark
    def test_actualizar_guepardo_benchmark(self, benchmark):
        # Primero creamos un guepardo
        nuevo_guepardo = Guepardo(nombre="Guepardo a Actualizar", edad=3, velocidad_maxima=110.0, habitat="Desierto")
        with app.app_context():
            db.session.add(nuevo_guepardo)
            db.session.commit()

        # Benchmarking para actualizar el guepardo
        def actualizar_guepardo():
            datos_actualizados = {
                "nombre": "Guepardo Actualizado",
                "edad": 4,
                "velocidad_maxima": 115.0,
                "habitat": "Sabana Actualizada"
            }
            return self.app.put(f'/guepardos/{nuevo_guepardo.id}', data=json.dumps(datos_actualizados), content_type='application/json')

        # Medimos el rendimiento
        result = benchmark(actualizar_guepardo)
        assert result.status_code == 200

    # Prueba de rendimiento para eliminar un guepardo
    @pytest.mark.benchmark
    def test_eliminar_guepardo_benchmark(self, benchmark):
        # Primero creamos un guepardo
        nuevo_guepardo = Guepardo(nombre="Guepardo a Eliminar", edad=3, velocidad_maxima=110.0, habitat="Desierto")
        with app.app_context():
            db.session.add(nuevo_guepardo)
            db.session.commit()

        # Benchmarking para eliminar el guepardo
        def eliminar_guepardo():
            return self.app.delete(f'/guepardos/{nuevo_guepardo.id}')

        # Medimos el rendimiento
        result = benchmark(eliminar_guepardo)
        assert result.status_code == 200

if __name__ == '__main__':
    unittest.main()
