import jwt
from application.settings import SECRET_KEY
import datetime

def encode_auth_token(username, isAdmin):
    """
    Generates the Auth Token
    :return: string
    """

    try:
        payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1000, seconds=5),
                   'iat': datetime.datetime.utcnow(),
                   'username': username,
                   'isAdmin': isAdmin
                   }
        return jwt.encode(payload,SECRET_KEY,algorithm='HS256')
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return {"username": payload["username"], "isAdmin": payload["isAdmin"]}
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'