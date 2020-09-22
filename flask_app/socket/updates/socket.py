from flask_app.socket import socket_io, ROOM
from flask_socketio import emit
from models import Person, DancingClass, Couple


@socket_io.on("person_updated")
def person_updated(person_id):
    person = Person.query.filter(Person.id == person_id).first()
    emit(
        "person_updated",
        person.json(include_active_partners=True),
        room=ROOM,
        include_self=False
    )


@socket_io.on("couple_updated")
def couple_updated(couple_id):
    couple = Couple.query.filter(Couple.id == couple_id).first()
    emit(
        "couple_updated",
        couple.json(),
        room=ROOM,
        include_self=False
    )


@socket_io.on("dancing_class_updated")
def dancing_class_updated(dancing_class_id):
    dancing_class = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
    emit(
        "dancing_class_updated",
        dancing_class.json(),
        room=ROOM,
        include_self=False
    )
