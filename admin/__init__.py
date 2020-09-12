from flask_admin import Admin
from .views import MyAdminIndexView, BaseView, UserView
from models import User, Role, UserRole, Person, DancingClass, DancingClassPerson, DancingClassCouple, Couple


admin = Admin(name="4hf Corona registration", template_mode="bootstrap3", index_view=MyAdminIndexView())


def init_app(app, db):
    admin.init_app(app)
    admin.add_view(UserView(User, db.session))
    admin.add_view(BaseView(Role, db.session))
    admin.add_view(BaseView(UserRole, db.session))
    admin.add_view(BaseView(Person, db.session))
    admin.add_view(BaseView(Couple, db.session))
    admin.add_view(BaseView(DancingClass, db.session))
    admin.add_view(BaseView(DancingClassPerson, db.session))
    admin.add_view(BaseView(DancingClassCouple, db.session))
