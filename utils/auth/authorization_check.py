from flask import request, abort
import jwt
from functools import wraps
from config.config import Config

def authorization_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            header = request.headers.get('Authorize')
            jwt.decode(header, Config.SECRET_KEY, algorithms=['HS256'])
        except:
            abort(400, description="Token is invalid")
        return f(*args, **kwargs)
    return decorator