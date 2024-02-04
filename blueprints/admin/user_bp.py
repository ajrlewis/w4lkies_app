from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from forms.user_form import UserForm
from models.user import User
from utils.security_utils import generate_confirmation_token

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/", methods=["GET"])
@user_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def get(user_id: int = None):
    user = None
    users = None
    user_form = UserForm()
    if user_id is None:
        users = User.query.order_by(desc(User.id)).all()
    else:
        user = User.query.get(user_id)
        if user:
            user_form.set_data_from_model(user)
        else:
            flash(f"User not found.", "error")
    return render_template(
        "admin/user.html",
        user=user,
        users=users,
        user_form=user_form,
    )


@user_bp.route("/add", methods=["POST"])
@login_required
def add():
    user_form = UserForm()
    if user_form.validate_on_submit():
        User.add(user_form.data)
        flash(f"User added successfully!", "success")
    return redirect(url_for("user_bp.get"))


@user_bp.route("/update/<int:user_id>", methods=["POST", "PUT"])
@login_required
def update(user_id: int):
    user = User.query.get(user_id)
    user_form = UserForm()
    if user and user_form.validate_on_submit():
        user.update(user_form.data)
        flash("User updated successfully!", "success")
    else:
        flash("User not found.", "error")
    return redirect(url_for("user_bp.get"))


@user_bp.route("/delete/<int:user_id>", methods=["POST", "DELETE"])
@login_required
def delete(user_id: int):
    user = User.query.get(user_id)
    if user:
        user.delete()
        flash("User deleted successfully!", "success")
    else:
        flash("User not found.", "error")
    return redirect(url_for("user_bp.get"))


@user_bp.route("/_add", methods=["GET", "POST"])
def _add():
    user_form = UserForm()
    if user_form.validate_on_submit():
        User.add(user_form.data)
        token = security_utils.generate_confirmation_token(user.email)
        confirm_url = url_for("user.confirm_email", token=token, _external=True)
        html = render_template("email/user_confirmation.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        email_utils.send(user.email, subject, html)
        flash("A confirmation email has been sent via email.", "success")
        return redirect(url_for("main.home"))

    return render_template("user/register.html", form=form)


@user_bp.route("/confirm/<string:token>")
@login_required
def confirm_email(token: str):
    try:
        email = security_utils.confirm_token(token)
        login_user(user)
    except:
        flash("The confirmation link is invalid or has expired.", "error")
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed. Please login.", "success")
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    return redirect(url_for("main.home"))
