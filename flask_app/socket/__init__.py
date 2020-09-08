from flask_socketio import SocketIO


socket_io = SocketIO()


def init_app(app):
    from .test import socket as test
    socket_io.init_app(app, cors_allowed_origins="*", async_mode="eventlet", message_queue=app.config.get("REDIS_URL"))
    # socket_io.init_app(app, cors_allowed_origins="*", async_mode="eventlet")
