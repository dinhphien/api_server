from functools import wraps
from .jw_token import decode_auth_token
from flask import request, current_app
from application.auth.service import AuthService


def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return {'message': 'Token is missing!'}, 401
        else:
            resp = decode_auth_token(token)
            if isinstance(resp, str):
                return {'message': resp}, 401
            else:
                if resp['isAdmin']:
                    user = AuthService.getAdmin(resp["username"])
                else:
                    user = AuthService.getUser(resp["username"])
                if not user:
                    return {'message': 'User does not exist. Please log in again'}, 401
        return f(*args, **kwargs)
    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return {'message': 'Token is missing!'}, 401
        else:
            resp = decode_auth_token(token)
            if not isinstance(resp, str):
                is_admin = resp['isAdmin']
                if not is_admin:
                    return {'message': "Require admin privilege!"}, 405
                admin = AuthService.getAdmin(resp["username"])
                if not admin:
                    return {'message': 'Admin account does not exist. Please log in again'}, 401
            else:
                return {'message': resp}, 401

        return f(*args, **kwargs)

    return decorated
