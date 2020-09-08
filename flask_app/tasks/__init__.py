from flask_app import create_app
from .example import *


rq_app = create_app()
rq_app.app_context().push()
