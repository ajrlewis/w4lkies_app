import json
from flask import Blueprint, flash, redirect, render_template, url_for
from forms.sign_up_form import SignUpForm
from utils.email_utils import send

sign_up_bp = Blueprint("sign_up_bp", __name__)


@sign_up_bp.route("/", methods=["GET"])
def get():
    form = SignUpForm()
    return render_template("public/sign_up.html", form=form)


@sign_up_bp.route("/", methods=["POST"])
def add():
    form = SignUpForm()
    if form.validate_on_submit():
        data = form.to_dict()
        html = render_template("email/sign_up.html", data=data)
        attachment = {
            "filename": "W4lkies Sign Up.json",
            "content_type": "application/json",
            "data": json.dumps(data),
            "disposition": "attachment",
        }
        attachments = [attachment]
        send(
            sender="hello@w4lkies.com",
            recipient=data["customer_email"],
            subject="🎉🎊 W4lkies Sign Up 🎉🎊",
            html=html,
            attachments=attachments,
        )
        flash("Sign up successful!", "success")
        return redirect(url_for("index_bp.get"))
    else:
        flash("Sign up not successful!", "error")
        return redirect(url_for("sign_up_bp.get"))
