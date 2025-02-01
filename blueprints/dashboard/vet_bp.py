from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import desc

from decorators import admin_user_required
from forms.vet_form import VetForm
from models.vet import Vet

vet_bp = Blueprint("vet_bp", __name__)


@vet_bp.route("/", methods=["GET"])
@vet_bp.route("/<int:vet_id>", methods=["GET"])
@login_required
def get(vet_id: int = None):
    vets = None
    vet = None
    vet_form = VetForm()
    if vet_id is None:
        # Is vet supplied in query parameters?
        vet_form_data = dict(request.args)
        if vet_form_data:
            vet_form.set_data_from_data(vet_form_data)

        vets = Vet.query.order_by(Vet.name).all()
    else:
        vet = Vet.query.get(vet_id)
        if vet:
            vet_form.set_data_from_model(vet)
        else:
            flash(f"Vet not found.", "error")

    return render_template(
        "dashboard/vet.html",
        vet=vet,
        vets=vets,
        vet_form=vet_form,
    )


@vet_bp.route("/add", methods=["POST"])
@login_required
def add():
    form = VetForm()
    if form.validate_on_submit():
        Vet.add(form.data)
        flash(f"Vet added successfully!", "success")
    return redirect(url_for("vet_bp.get"))


@vet_bp.route("/update/<int:vet_id>", methods=["POST", "PUT"])
@login_required
def update(vet_id: int):
    vet = Vet.query.get(vet_id)
    form = VetForm()
    if vet and form.validate_on_submit():
        vet.update(form.data)
        flash("Vet updated successfully!", "success")
    else:
        flash("Vet not found.", "error")
    return redirect(url_for("vet_bp.get"))


@vet_bp.route("/delete/<int:vet_id>", methods=["POST", "DELETE"])
@login_required
def delete(vet_id: int):
    vet = Vet.query.get(vet_id)
    if vet:
        vet.delete()
        flash("Vet deleted successfully!", "success")
    else:
        flash("Vet not found.", "error")
    return redirect(url_for("vet_bp.get"))
