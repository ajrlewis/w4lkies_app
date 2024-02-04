from flask import Blueprint, render_template
from sqlalchemy import desc
from models.service import Service

about_bp = Blueprint("about_bp", __name__)


@about_bp.route("/", methods=["GET"])
def get():
    services = (
        Service.query.filter_by(is_active=True).order_by(desc(Service.price)).all()
    )
    print(f"{services = }")
    return render_template("public/about.html"), 200
    # return render_template("public/about-ui.html"), 200
