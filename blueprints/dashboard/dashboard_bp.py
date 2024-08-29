from flask import Blueprint, jsonify, render_template
from flask_login import login_required

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/", methods=["GET"])
@login_required
def get():
    return render_template("dashboard/dashboard.html")
