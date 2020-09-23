from flask_socketio import SocketIO, join_room, leave_room
from models.base import decode_token
from models.user.model import get_user_from_token_data
from flask import request


ROOM = "update_room"


socket_io = SocketIO()


def init_app(app):
    from .test import socket as test
    from .updates import socket as updates
    socket_io.init_app(app, cors_allowed_origins=app.config["ALLOWED_URLS"])


@socket_io.on("connect")
def test_connect():
    token = request.args.get("token", None)
    if token:
        user = get_user_from_token_data(decode_token(token))
        if user:
            join_room(ROOM)


@socket_io.on("disconnect")
def test_disconnect():
    leave_room(ROOM)
