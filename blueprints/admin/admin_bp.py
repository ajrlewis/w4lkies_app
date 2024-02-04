from flask import Blueprint, jsonify, render_template
from flask_login import login_required

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/", methods=["GET"])
@login_required
def get():
    return render_template("admin/admin.html")
