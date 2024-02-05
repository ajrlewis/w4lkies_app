from flask import Blueprint, render_template
from sqlalchemy import desc
from models.service import Service

about_bp = Blueprint("about_bp", __name__)


@about_bp.route("/", methods=["GET"])
def get():
    services = (
        Service.query.filter_by(is_active=True).order_by(desc(Service.price)).all()
    )
    return render_template("public/about.html", services=services), 200
