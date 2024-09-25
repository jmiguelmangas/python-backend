from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import User  # Ahora importamos desde models.py


def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            claims = get_jwt()
            if claims['role'] != required_role:
                return {'error': 'Access denied'}, 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper
