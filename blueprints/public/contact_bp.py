from flask import Blueprint, render_template

contact_bp = Blueprint("contact_bp", __name__)


@contact_bp.route("/", methods=["GET"])
def get():
    return render_template("public/contact.html"), 200
