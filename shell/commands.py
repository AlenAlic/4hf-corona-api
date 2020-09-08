from ext import db
from models import User
from models.user.constants import ACCESS_ADMIN


def shell_commands():
    return create_admin, set_password


def create_admin(email, password, first_name=None, last_name=None):
    usr = User(email, password)
    usr.first_name = first_name
    usr.last_name = last_name
    usr.access = ACCESS_ADMIN
    usr.is_active = True
    db.session.add(usr)
    db.session.commit()


def set_password(email, password):
    usr = User.query.filter(User.email.ilike(email)).first()
    if usr is not None:
        usr.set_password(password)
        db.session.commit()
    else:
        print(f"Could not find user with email: '{email}'")
