from functools import wraps

from flask import request
from orchestrator.settings import SECRET_KEY


def secret_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get("X-Orchestryzi-Token") == SECRET_KEY:
            return f(*args, **kwargs)
        return {"msg": "You are not authorized to perform this action"}, 401
    return decorated_function

def secret_key_maybe_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not SECRET_KEY:
            return f(*args, **kwargs)
            
        if request.headers.get("X-Orchestryzi-Token") == SECRET_KEY:
            return f(*args, **kwargs)
        return {"msg": "You are not authorized to perform this action"}, 401
    return decorated_function