from ext import db
from models.tables import TABLE_PERSON, TABLE_DANCING_CLASS_PERSON
from models import TrackModifications


class Person(db.Model, TrackModifications):
    __tablename__ = TABLE_PERSON
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    student_number = db.Column(db.String(16), nullable=True)
    dancing_classes = db.relationship("DancingClass", secondary=TABLE_DANCING_CLASS_PERSON)
    dancing_class_persons = db.relationship("DancingClassPerson", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def active_partners(self):
        return [partner for partners in [dcp.partners for dcp in self.dancing_class_persons] for partner in partners]

    def json(self, include_active_partners=False):
        data = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "student_number": self.student_number,
        }
        if include_active_partners:
            data.update({
                "active_partners": [p.full_name for p in self.active_partners],
            })
        return data
