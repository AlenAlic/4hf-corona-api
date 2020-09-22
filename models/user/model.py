from ext import db, login
from models.tables import TABLE_USERS, TABLE_USER_ROLE
from models import TrackModifications
from models.base import get_token_from_request
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from .constants import ACCESS_ADMIN, ACCESS_BOARD, ACCESS_USER
from werkzeug.security import generate_password_hash, check_password_hash
from constants import SECONDS_DAY, SECONDS_QUARTER
from jwt import encode, decode
from jwt.exceptions import InvalidTokenError
from time import time
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


class Anonymous(AnonymousUserMixin):

    @hybrid_property
    def is_admin(self):
        return False

    @hybrid_property
    def is_board(self):
        return False

    @property
    def role_names(self):
        return []

    @property
    def profile(self):
        return {}

    def json(self):
        return self.profile


def get_user_from_token_data(data):
    if data is not None:
        try:
            user_id = data["id"]
            reset_index = data["reset_index"]
            return User.query.filter(User.id == user_id, User.reset_index == reset_index).first()
        except (InvalidTokenError, AttributeError, KeyError):
            return None
    return None


@login.request_loader
def load_user(req):
    return get_user_from_token_data(get_token_from_request(req))


@login.user_loader
def load_user(user_id):
    try:
        user_id, reset_index = user_id.split("-")
        return User.query.filter(User.id == user_id, User.reset_index == reset_index).first()
    except (AttributeError, ValueError):
        return None


class User(UserMixin, db.Model, TrackModifications, Anonymous):
    __tablename__ = TABLE_USERS
    id = db.Column(db.Integer, primary_key=True)
    reset_index = db.Column(db.Integer, nullable=False, default=0)
    email = db.Column(db.String(128), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer, nullable=False, default=ACCESS_USER)
    activation_code = db.Column(db.String(128), unique=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    roles = db.relationship("Role", secondary=TABLE_USER_ROLE)

    def get_id(self):
        return f"{self.id}-{self.reset_index}"

    def __repr__(self):
        return f"{self.email}"

    def __init__(self, email=None, password=None):
        self.email = email
        if password:
            self.set_password(password)

    def set_password(self, password, increment=True):
        self.password_hash = generate_password_hash(password)
        if self.reset_index is not None and increment:
            self.reset_index += 1

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=SECONDS_QUARTER):
        return encode({
            "reset_password": self.id,
            "exp": time() + expires_in
        }, current_app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])["reset_password"]
        except InvalidTokenError:
            return None
        return User.query.get(user_id)

    @hybrid_property
    def is_admin(self):
        return self.access == ACCESS_ADMIN

    @hybrid_property
    def is_board(self):
        return self.access == ACCESS_BOARD

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def role_names(self):
        return [r.name for r in self.roles]

    @property
    def profile(self):
        data = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "roles": [r.json() for r in self.roles],
        }
        return data

    def get_auth_token(self, expires_in=SECONDS_DAY):
        return encode({
            "id": self.id,
            "reset_index": self.reset_index,
            "email": self.email,
            "access": self.access,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "roles": [r.json() for r in self.roles],
            "iat": time(),
            "exp": time() + expires_in,
        }, current_app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")
