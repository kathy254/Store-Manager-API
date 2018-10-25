import jwt

from flask import request
from functools import wraps
from instance.config import secret_key


def get_token(f):
    @wraps(f)
    def decorated(*arg, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return {'result': 'no token found'}, 401
        try:
            token = jwt.decode(token, secret_key, algorithm='HS256'), 401
        except:
            return {'result': 'Invalid token'}, 401
        return f(*arg, **kwargs)
    return decorated