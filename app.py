from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Configuración de la aplicación
app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guepardos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir el modelo Guepardo
class Guepardo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    velocidad_maxima = db.Column(db.Float, nullable=False)
    habitat = db.Column(db.String(200), nullable=False)

# Crear las tablas
with app.app_context():
    db.create_all()

# Rutas y Métodos CRUD

# Crear un nuevo guepardo (Create)
@app.route('/guepardos', methods=['POST'])
def create_guepardo():
    data = request.get_json()
    nombre = data.get('nombre')
    edad = data.get('edad')
    velocidad_maxima = data.get('velocidad_maxima')
    habitat = data.get('habitat')

    if not nombre or not edad or not velocidad_maxima or not habitat:
        return jsonify({"error": "Datos incompletos"}), 400

    nuevo_guepardo = Guepardo(nombre=nombre, edad=edad, velocidad_maxima=velocidad_maxima, habitat=habitat)
    db.session.add(nuevo_guepardo)
    db.session.commit()

    return jsonify({"message": "Guepardo creado exitosamente", "guepardo": {"id": nuevo_guepardo.id, "nombre": nuevo_guepardo.nombre, "edad": nuevo_guepardo.edad, "velocidad_maxima": nuevo_guepardo.velocidad_maxima, "habitat": nuevo_guepardo.habitat}}), 201

# Obtener todos los guepardos (Read)
@app.route('/guepardos', methods=['GET'])
def get_guepardos():
    guepardos = Guepardo.query.all()
    result = [{"id": guepardo.id, "nombre": guepardo.nombre, "edad": guepardo.edad, "velocidad_maxima": guepardo.velocidad_maxima, "habitat": guepardo.habitat} for guepardo in guepardos]

    return jsonify(result), 200

# Obtener un guepardo por ID (Read)
@app.route('/guepardos/<int:id>', methods=['GET'])
def get_guepardo(id):
    guepardo = Guepardo.query.get(id)
    if not guepardo:
        return jsonify({"error": "Guepardo no encontrado"}), 404

    return jsonify({"id": guepardo.id, "nombre": guepardo.nombre, "edad": guepardo.edad, "velocidad_maxima": guepardo.velocidad_maxima, "habitat": guepardo.habitat}), 200

# Actualizar un guepardo por ID (Update)
@app.route('/guepardos/<int:id>', methods=['PUT'])
def update_guepardo(id):
    guepardo = Guepardo.query.get(id)
    if not guepardo:
        return jsonify({"error": "Guepardo no encontrado"}), 404

    data = request.get_json()
    guepardo.nombre = data.get('nombre', guepardo.nombre)
    guepardo.edad = data.get('edad', guepardo.edad)
    guepardo.velocidad_maxima = data.get('velocidad_maxima', guepardo.velocidad_maxima)
    guepardo.habitat = data.get('habitat', guepardo.habitat)

    db.session.commit()

    return jsonify({"message": "Guepardo actualizado exitosamente", "guepardo": {"id": guepardo.id, "nombre": guepardo.nombre, "edad": guepardo.edad, "velocidad_maxima": guepardo.velocidad_maxima, "habitat": guepardo.habitat}}), 200

# Eliminar un guepardo por ID (Delete)
@app.route('/guepardos/<int:id>', methods=['DELETE'])
def delete_guepardo(id):
    guepardo = Guepardo.query.get(id)
    if not guepardo:
        return jsonify({"error": "Guepardo no encontrado"}), 404

    db.session.delete(guepardo)
    db.session.commit()

    return jsonify({"message": "Guepardo eliminado exitosamente"}), 200

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
