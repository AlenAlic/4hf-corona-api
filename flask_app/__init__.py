from flask import Flask
from flask_login import current_user
from ext import db, migrate, login, mail, cors
from config import Config


def create_app(config_class=Config):
    from datetime import datetime

    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False

    # Extensions
    configure_extensions(app)

    # Shell commands
    from shell import shell_commands

    @app.shell_context_processor
    def make_shell_context():
        return {f.__name__: f for f in shell_commands()}

    # Update when a authenticated user was last seen before each request
    @app.before_request
    def before_request_callback():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    # Add missing roles on startup
    from models.roles import update_roles
    with app.app_context():
        update_roles()

    # Register blueprints, API, and sockets
    register_blueprints(app)

    # Background tasks
    # noinspection PyTypeChecker
    register_task_queues(app)

    "Monkey patch for HTTPS Swagger"
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    return app


def configure_extensions(app):
    from models import Anonymous
    import admin
    from flask_app import socket
    import commands

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:"))
    login.init_app(app)
    login.login_view = "main.index"
    login.login_message = None
    login.anonymous_user = Anonymous
    admin.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    socket.init_app(app)
    commands.init_app(app)


def register_blueprints(app):
    from flask_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from flask_app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from flask_app.email import bp as email_bp
    app.register_blueprint(email_bp, url_prefix="/email")

    import apis
    apis.init_app(app)


def register_task_queues(app):
    from redis import Redis
    import rq

    queues = app.config["RQ_WORKERS"]
    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.task_queues = {
        queue: rq.Queue(queue, connection=app.redis, decode_responses=True) for queue in queues
    }
