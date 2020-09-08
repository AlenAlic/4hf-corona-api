from datetime import datetime
from constants import DATETIME_FORMAT
from random import choice
from string import ascii_letters


def datetime_python(s):
    return datetime.strptime(s, DATETIME_FORMAT)


def activation_code():
    allowed_chars = ascii_letters + '0123456789'
    token = ''.join([choice(allowed_chars) for _ in range(128)])
    token += str(int(datetime.utcnow().timestamp() * 10**6))
    return token[-128:]
