from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from flask_app.main import bp
from flask_app.main.forms import LoginForm, AddUserForm
from models import User, requires_access_level
from models.user.constants import ACCESS_ADMIN, ACCESS_BOARD, ACCESS_USER
from constants import GET, POST
import os
from ext import db
from apis.auth.email import send_activation_email
from utilities import activation_code


@bp.route("/", methods=[GET, POST])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if request.method == POST:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid email or password", "danger")
                return redirect(url_for("main.index"))
            if user.is_active and (user.is_admin or user.is_board):
                login_user(user)
                return redirect(url_for("main.dashboard"))
            else:
                flash("Account inactive", "warning")
                return redirect(url_for("main.index"))
    return render_template("main/index.html", login_form=form)


@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, "static"), "favicon.ico")


@bp.route("/dashboard", methods=[GET, POST])
@login_required
def dashboard():
    return render_template("main/dashboard.html")


@bp.route("/users", methods=[GET, POST])
@login_required
@requires_access_level(ACCESS_ADMIN, ACCESS_BOARD)
def users():
    form = AddUserForm()
    if request.method == POST:
        if form.validate_on_submit():
            user = User()
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.activation_code = activation_code()
            user.access = ACCESS_USER
            db.session.add(user)
            db.session.commit()
            send_activation_email(user)
            flash(f"Added account for {user.full_name} ({user.email})")
            return redirect(url_for("main.users"))
    return render_template("main/users.html", form=form)


@bp.route("/logout", methods=[GET])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
