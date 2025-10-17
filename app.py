from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import os
import requests
from flask_cors import CORS
CORS(app)



logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.logger.debug(f"Conectando a la base con: {app.config['SQLALCHEMY_DATABASE_URI']}")

# DEFINIR db ANTES DE USARLO
db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Crear tablas
with app.app_context():
    db.create_all()

# Ruta principal
@app.route('/')
def index():
    app.logger.debug("Recibí una petición en /")
    return 'Backend funcionando correctamente'

# Crear usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo_usuario = Usuario(nombre=data['nombre'], email=data['email'])
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Enviar notificación al microservicio
    try:
        mensaje = {'mensaje': f"Usuario {nuevo_usuario.nombre} creado correctamente"}
        r = requests.post('http://notificaciones:5000/notify', json=mensaje)
        app.logger.debug(f"Notificación enviada: {r.status_code}")
    except Exception as e:
        app.logger.error(f"Error al enviar notificación: {e}")

    return jsonify({'mensaje': 'Usuario creado correctamente'}), 201


# Listar usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    resultado = [{'id': u.id, 'nombre': u.nombre, 'email': u.email} for u in usuarios]
    return jsonify(resultado)

# Ejecutar servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
