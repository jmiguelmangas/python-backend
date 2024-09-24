from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = SECRET_KEY  # Cambia esto por una clave secreta más segura
jwt = JWTManager(app)

# Configuración de SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos y Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.get(identity)
    return {'role': user.role}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # Agregamos el rol


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role', 'user')  # Por defecto, el rol es 'user'
    
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Busca el usuario en la base de datos
    user = User.query.filter_by(username=username).first()

    # Verifica si el usuario existe y si la contraseña es correcta
    if user and user.password == password:  # Recuerda que deberías usar hashing para contraseñas en producción
        access_token = create_access_token(identity=user.id)  # Usa el ID del usuario
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()  # Este decorador asegura que solo los usuarios autenticados puedan acceder
def protected():
    current_user = get_jwt_identity()  # Obtiene la identidad del usuario desde el token
    return jsonify(logged_in_as=current_user), 200

# Manejo de errores para el método POST
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

# Manejo de errores para el método PUT
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': str(error)}), 404

# Manejo de errores generales
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500



# Definir el modelo de Tarea
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    done = db.Column(db.Boolean, default=False)

    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done

# Esquema de la Tarea (para serialización)
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'done')

# Inicializar los esquemas
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Endpoint para obtener todas las tareas
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.query.all()
    return tasks_schema.jsonify(tasks)

# Endpoint para crear una tarea nueva
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return bad_request('El campo "title" es requerido.')  # Error si faltan datos
    new_task = Task(title=data['title'], description=data.get('description'), done=data.get('done', False))
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task), 201

@app.route('/tasks/check', methods=['GET'])
def check_tasks():
    tasks = Task.query.all()
    return jsonify({'count': len(tasks)})

# Eliminar una tarea por ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)  # Obtener la tarea o devolver 404
    db.session.delete(task)  # Eliminar la tarea de la base de datos
    db.session.commit()  # Guardar los cambios en la base de datos
    return '', 204  # Devolver un estado 204 No Content

# Actualizar una tarea por ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'done' in data:
        task.done = data['done']
    db.session.commit()
    return task_schema.jsonify(task)


if __name__ == "__main__":
    with app.app_context():  # Establecer el contexto de la aplicación
        db.create_all()      # Crear las tablas de la base de datos

    # Ejecutar la aplicación
    app.run(debug=True)