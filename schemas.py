from flask_marshmallow import Marshmallow
from models import Task  # Asegúrate de que Task esté importado desde el archivo models.py

ma = Marshmallow()  # Inicializa Marshmallow

# Esquema de la Tarea (para serialización)
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task  # Asigna el modelo Task
        load_instance = True  # Permite cargar instancias de SQLAlchemy
