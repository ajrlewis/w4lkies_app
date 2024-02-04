from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from forms.sign_in_form import SignInForm
from models.user import User
from utils.email_utils import send


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(int(user_id))


auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    form = SignInForm()
    if request.method == "GET":
        return render_template("admin/auth.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash("Please check your login details and try again.", "error")
                return redirect(url_for("auth_bp.sign_in"))
            now = datetime.now().strftime("%H:%M %Y-%m-%d")
            user_agent = request.user_agent.string
            ip_address = request.remote_addr
            html = render_template(
                "email/sign_in_notification.html",
                user=user,
                now=now,
                user_agent=user_agent,
                ip_address=ip_address,
            )
            send(
                sender="hello@w4lkies.com",
                recipient=email,
                subject="⚠️🔒 Sign-in Notification ⚠️🔒",
                html=html,
            )
            login_user(user, remember=True)
            next_page = request.form.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("admin_bp.get"))
        flash("Please check your login details and try again.", "error")
        return redirect(url_for("auth_bp.sign_in"))


@auth_bp.route("/sign-out", methods=["GET"])
@login_required
def sign_out():
    logout_user()
    flash("Signed out successfully.", "success")
    return redirect(url_for("auth_bp.sign_in"))
