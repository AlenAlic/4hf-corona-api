from ext import db
from models.tables import TABLE_DANCING_CLASS_PERSON, TABLE_DANCING_CLASS, TABLE_PERSON
from models import TrackModifications


class DancingClassPerson(db.Model, TrackModifications):
    __tablename__ = TABLE_DANCING_CLASS_PERSON
    __table_args__ = (db.UniqueConstraint("dancing_class_id", "person_id", name="_dancing_class_person_uc"),)
    id = db.Column(db.Integer(), primary_key=True)
    dancing_class_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_DANCING_CLASS}.id", ondelete="CASCADE"),
                                 nullable=False)
    dancing_class = db.relationship("DancingClass", lazy=False)
    person_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_PERSON}.id", ondelete="CASCADE"), nullable=False)
    person = db.relationship("Person", lazy=False)
    passed_triage = db.Column(db.Boolean, nullable=False, default=True)
    notes = db.Column(db.String(256), nullable=True)
    dancing_class_couples_leads = db.relationship("DancingClassCouple", foreign_keys="DancingClassCouple.person_id",
                                                  cascade="all, delete, delete-orphan", lazy=False)
    dancing_class_couples_follows = db.relationship("DancingClassCouple", foreign_keys="DancingClassCouple.partner_id",
                                                    cascade="all, delete, delete-orphan", lazy=False)

    def __repr__(self):
        return f"{self.person} - {self.dancing_class}"

    @property
    def partners(self):
        return [dcc.partner.person for dcc in self.dancing_class_couples_leads] + \
               [dcc.person.person for dcc in self.dancing_class_couples_follows]

    def json(self):
        data = {
            "id": self.id,
            "person": {
                "id": self.person.id,
            },
            "email": self.person.email,
            "full_name": self.person.full_name,
            "student_number": self.person.student_number,
            "passed_triage": self.passed_triage,
            "notes": self.notes,
        }
        return data
