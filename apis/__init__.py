from flask import Blueprint
from flask_restx import Api
from .auth import api as auth
from .ping import api as ping
from .user import api as user
from .dancing_class import api as dancing_class
from .person import api as person
from .couple import api as couple


authorizations = {
    "bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}


bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp, doc="/doc", authorizations=authorizations, security="bearer",
          title="Flask Boilerplate API", version="1.0")


api.add_namespace(auth)
api.add_namespace(couple)
api.add_namespace(dancing_class)
api.add_namespace(person)
api.add_namespace(user)
api.add_namespace(ping)


def init_app(app):
    from .debug import api as debug
    if app.config.get("DEBUG"):
        api.add_namespace(debug)
    app.register_blueprint(bp)
