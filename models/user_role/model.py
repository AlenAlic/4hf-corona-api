from ext import db
from models.tables import TABLE_USER_ROLE, TABLE_USERS, TABLE_ROLES
from models import TrackModifications


class UserRole(db.Model, TrackModifications):
    __tablename__ = TABLE_USER_ROLE
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_USERS}.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey(f"{TABLE_ROLES}.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"{self.user_id}-{self.role_id}"
