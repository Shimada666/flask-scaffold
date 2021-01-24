from functools import wraps

from flask import current_app, g, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models.user import User
from app.exceptions import AuthFailedException


def generate_token(user):
    expiration = 60 * 60 * 24 * 15
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('ascii')
    return token, expiration


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except Exception:
        return False
    user = User.query.get_or_404(data['id'])
    if user is None:
        return False
    g.current_user = user
    return True


def get_token():
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)
        except ValueError:
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()
        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                return AuthFailedException(msg='The token type must be bearer.')
            if token is None:
                return AuthFailedException(msg='missing the token.')
            if not validate_token(token):
                return AuthFailedException(msg='the token was invalid.')
        return f(*args, **kwargs)

    return decorated
