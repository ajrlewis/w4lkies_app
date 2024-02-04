from flask import Blueprint, render_template

legal_bp = Blueprint("legal_bp", __name__)


@legal_bp.route("/", methods=["GET"])
def get():
    return render_template("public/legal.html"), 200
