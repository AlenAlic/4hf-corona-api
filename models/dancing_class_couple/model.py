from ext import db
from models.tables import TABLE_DANCING_CLASS_COUPLE, TABLE_DANCING_CLASS, TABLE_DANCING_CLASS_PERSON
from models import TrackModifications


class DancingClassCouple(db.Model, TrackModifications):
    __tablename__ = TABLE_DANCING_CLASS_COUPLE
    __table_args__ = (
        db.UniqueConstraint("dancing_class_id", "person_id", "partner_id", name="_dancing_class_couple_uc"),
    )
    id = db.Column(db.Integer(), primary_key=True)
    dancing_class_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_DANCING_CLASS}.id", ondelete="CASCADE"))
    dancing_class = db.relationship("DancingClass")
    person_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_DANCING_CLASS_PERSON}.id", ondelete="CASCADE"))
    person = db.relationship("DancingClassPerson", foreign_keys=person_id)
    partner_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_DANCING_CLASS_PERSON}.id", ondelete="CASCADE"))
    partner = db.relationship("DancingClassPerson", foreign_keys=partner_id)

    def __repr__(self):
        return f"{self.person} - {self.partner}"

    def json(self):
        data = {
            "id": self.id,
            "lead": self.person.json(),
            "follow": self.partner.json(),
        }
        return data
