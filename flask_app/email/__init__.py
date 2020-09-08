from flask import Blueprint

bp = Blueprint("email", __name__)

from flask_app.email import routes
