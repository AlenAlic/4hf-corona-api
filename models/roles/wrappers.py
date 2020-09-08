from functools import wraps
from flask_login import current_user
from http import HTTPStatus


def requires_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role_names not in roles:
                return "", HTTPStatus.FORBIDDEN.value
            return f(*args, **kwargs)
        return decorated_function
    return decorator
