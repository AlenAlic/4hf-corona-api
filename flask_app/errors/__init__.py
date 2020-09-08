from flask import Blueprint

bp = Blueprint("errors", __name__)

from flask_app.errors import handlers
