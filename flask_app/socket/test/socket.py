from flask_app.socket import socket_io
from flask_socketio import emit


@socket_io.on("echo")
def echo(message):
    """Echo"""
    emit(
        "echo",
        message
    )
