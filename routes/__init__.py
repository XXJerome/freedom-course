import uuid
from functools import wraps

import redis
from flask import (
    request,
    abort,
)

from models.user import User
from utils import log

session = redis.StrictRedis()
csrf_tokens = redis.StrictRedis()


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        uid = int(session.get(session_id))
    else:
        uid = -1
    u = User.one(id=uid)
    return u


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        if token in str(csrf_tokens.keys()) and int(csrf_tokens.get(token)) == u.id:
            # token 失效（一次性）
            csrf_tokens.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens.set(token, u.id)
    return token
