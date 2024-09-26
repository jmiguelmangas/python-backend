from flask_marshmallow import Marshmallow
from models import Task, Tag  # Asegúrate de que Task y Tag estén importados desde el archivo models.py

ma = Marshmallow()  # Inicializa Marshmallow

# Esquema de la Etiqueta (para serialización)
class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag  # Asigna el modelo Tag
        load_instance = True  # Permite cargar instancias de SQLAlchemy

# Esquema de la Tarea (para serialización)
class TaskSchema(ma.SQLAlchemyAutoSchema):
    tags = ma.Nested(TagSchema, many=True)  # Incluir las etiquetas en el esquema

    class Meta:
        model = Task  # Asigna el modelo Task
        load_instance = True  # Permite cargar instancias de SQLAlchemy
