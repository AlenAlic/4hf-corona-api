from ext import db
from models.tables import TABLE_ROLES
from models import TrackModifications


class Role(db.Model, TrackModifications):
    __tablename__ = TABLE_ROLES
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"

    def __init__(self, name):
        self.name = name

    def json(self):
        data = {
            "id": self.id,
            "name": self.name,
        }
        return data
