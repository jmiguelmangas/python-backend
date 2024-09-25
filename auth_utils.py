from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User  # Ahora importamos desde models.py

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if user and user.role == required_role:
                return func(*args, **kwargs)
            else:
                return jsonify({"error": "Access forbidden: insufficient permissions"}), 403
        return wrapper
    return decorator