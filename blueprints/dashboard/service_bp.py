from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy import desc

from decorators import admin_user_required
from forms.service_form import ServiceForm
from models.service import Service

service_bp = Blueprint("service_bp", __name__)


@service_bp.route("/", methods=["GET"])
@service_bp.route("/<int:service_id>", methods=["GET"])
@login_required
@admin_user_required
def get(service_id: int = None):
    services = None
    service = None
    service_form = ServiceForm()
    if service_id is None:
        services = (
            Service.query.filter_by(is_active=True).order_by(desc(Service.id)).all()
        )
    else:
        service = Service.query.get(service_id)
        if service:
            service_form.set_data_from_model(service)
        else:
            flash(f"Service not found.", "error")
    return render_template(
        "dashboard/service.html",
        service=service,
        services=services,
        service_form=service_form,
    )


@service_bp.route("/add", methods=["POST"])
@login_required
@admin_user_required
def add():
    form = ServiceForm()
    if form.validate_on_submit():
        data = form.data | {"is_active": True}
        Service.add(data)
        flash(f"Service added successfully!", "success")
    return redirect(url_for("service_bp.get"))


@service_bp.route("/update/<int:service_id>", methods=["POST", "PUT"])
@login_required
@admin_user_required
def update(service_id: int):
    service = Service.query.get(service_id)
    form = ServiceForm()
    if service and form.validate_on_submit():
        service.update(form.data)
        flash("Service updated successfully!", "success")
    else:
        flash("Service not found.", "error")
    return redirect(url_for("service_bp.get"))


@service_bp.route("/delete/<int:service_id>", methods=["POST", "DELETE"])
@login_required
@admin_user_required
def delete(service_id: int):
    service = Service.query.get(service_id)
    if service:
        service.delete()
        flash("Service deleted successfully!", "success")
    else:
        flash("Service not found.", "error")
    return redirect(url_for("service_bp.get"))
