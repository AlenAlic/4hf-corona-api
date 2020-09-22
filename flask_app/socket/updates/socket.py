from flask_app.socket import socket_io, ROOM
from flask_socketio import emit
from models import Person, DancingClass, Couple
from apis.person.apis import all_persons
from apis.couple.apis import all_couples
from apis.dancing_class.apis import all_dancing_classes


@socket_io.on("person_created")
def person_created():
    emit(
        "person_created",
        all_persons(),
        room=ROOM,
        include_self=False
    )


@socket_io.on("person_updated")
def person_updated(person_id):
    person = Person.query.filter(Person.id == person_id).first()
    emit(
        "person_updated",
        person.json(include_active_partners=True),
        room=ROOM,
        include_self=False
    )


@socket_io.on("person_deleted")
def person_deleted(person_id):
    emit(
        "person_deleted",
        person_id,
        room=ROOM,
        include_self=False
    )


@socket_io.on("couple_created")
def couple_created():
    emit(
        "couple_created",
        all_couples(),
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


@socket_io.on("couple_deleted")
def couple_deleted(couple_id):
    emit(
        "couple_deleted",
        couple_id,
        room=ROOM,
        include_self=False
    )


@socket_io.on("dancing_class_created")
def dancing_class_created():
    emit(
        "dancing_class_created",
        all_dancing_classes(),
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


@socket_io.on("dancing_class_deleted")
def dancing_class_deleted(dancing_class_id):
    emit(
        "dancing_class_deleted",
        dancing_class_id,
        room=ROOM,
        include_self=False
    )
