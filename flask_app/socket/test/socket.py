from flask_app.socket import socket_io
from flask_socketio import emit
from flask import request


@socket_io.on("connect")
def connect():
    # noinspection PyUnresolvedReferences
    sid = request.sid
    emit(
        "connected",
        "Connected with server",
        room=sid
    )


@socket_io.on("echo")
def echo(message):
    """Echo"""
    emit(
        "echo",
        message
    )
