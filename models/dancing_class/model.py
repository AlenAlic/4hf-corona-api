from ext import db
from models.tables import TABLE_DANCING_CLASS
from models import TrackModifications
from datetime import datetime


class DancingClass(db.Model, TrackModifications):
    __tablename__ = TABLE_DANCING_CLASS
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    attendees = db.relationship("DancingClassPerson", cascade="all, delete, delete-orphan")
    couples = db.relationship("DancingClassCouple", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"{self.name} ({self.datetime_string})"

    @property
    def datetime_string(self):
        return self.datetime.strftime("%d-%m-%Y %H:%M")

    @property
    def person_ids(self):
        lead_ids = [c.person.person.id for c in self.couples]
        follow_ids = [c.partner.person.id for c in self.couples]
        return lead_ids + follow_ids

    def json(self, include_attendees: bool = False):
        data = {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime.isoformat(),
        }
        if include_attendees:
            data.update({
                "attendees": [p.json() for p in sorted(self.attendees, key=lambda a: a.person.first_name)],
                "couples": [p.json() for p in sorted(self.couples, key=lambda a: a.person.person.first_name)],
                "person_ids": self.person_ids
            })
        return data
