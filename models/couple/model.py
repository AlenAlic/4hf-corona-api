from ext import db
from models.tables import TABLE_COUPLE, TABLE_PERSON
from models import TrackModifications


class Couple(db.Model, TrackModifications):
    __tablename__ = TABLE_COUPLE
    __table_args__ = (
        db.UniqueConstraint("lead_id", "follow_id", name="_lead_follow_uc"),
    )
    id = db.Column(db.Integer(), primary_key=True)
    lead_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_PERSON}.id", ondelete="CASCADE"))
    lead = db.relationship("Person", foreign_keys=lead_id)
    follow_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_PERSON}.id", ondelete="CASCADE"))
    follow = db.relationship("Person", foreign_keys=follow_id)

    def __repr__(self):
        return f"{self.lead}-{self.follow}"

    def json(self):
        data = {
            "id": self.id,
            "lead": self.lead.json(),
            "follow": self.follow.json(),
        }
        return data
