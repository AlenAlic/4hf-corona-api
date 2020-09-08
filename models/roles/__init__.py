from .model import Role
from models.base import table_exists


def update_roles():
    if table_exists(Role):
        from ext import db
        from .constants import ROLES

        all_roles = set(ROLES)
        existing_roles = set([r.name for r in Role.query.all()])
        missing_roles = all_roles.difference(existing_roles)
        for name in missing_roles:
            db.session.add(Role(name))
        db.session.commit()
