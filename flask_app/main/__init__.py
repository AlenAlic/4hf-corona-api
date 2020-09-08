from flask import Blueprint

bp = Blueprint("main", __name__)

from flask_app.main import routes
