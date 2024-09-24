from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os



app = Flask(__name__)

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

# Configuración de SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos y Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

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