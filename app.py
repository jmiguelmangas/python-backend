from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

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
    title = request.json['title']
    description = request.json.get('description', "")
    new_task = Task(title, description, False)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task), 201

# Otros endpoints se pueden modificar de manera similar...

if __name__ == "__main__":
    with app.app_context():  # Establecer el contexto de la aplicación
        db.create_all()      # Crear las tablas de la base de datos

    # Ejecutar la aplicación
    app.run(debug=True)