from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    except Exception as e:
        return str(e)  # Catch other JWT exceptions and return the error message

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'][7:]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        current_user_id = decode_token(token)
        if isinstance(current_user_id, str):
            return jsonify({"message": current_user_id}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated
