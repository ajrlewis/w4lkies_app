import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from loguru import logger
from PIL import Image
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from decorators import admin_user_required
from forms.dog_form import DogForm
from models.dog import Dog
from services import dog_service

dog_bp = Blueprint("dog_bp", __name__)


# @dog_bp.route("/", methods=["GET"])
# @dog_bp.route("/<int:dog_id>", methods=["GET"])
# @login_required
# def get(dog_id: int = None):
#     dogs = None
#     dog = None
#     dog_form = DogForm()
#     if dog_id is None:
#         dogs = dog_service.get_dogs()
#     else:
#         dog = dog_service.get_dog(dog_id)
#         if dog:
#             dog_form.set_data_from_model(dog)
#         else:
#             flash(f"Dog not found.", "error")
#     logger.debug(f"{dog = }")
#     logger.debug(f"{dogs = }")
#     logger.debug(f"{dog_form = }")
#     return render_template(
#         "dashboard/dog.html",
#         dog=dog,
#         dogs=dogs,
#         dog_form=dog_form,
#     )


@dog_bp.route("/", methods=["GET"])
@login_required
def get_all():
    dog_form = DogForm()
    dogs = dog_service.get_dogs()
    logger.debug(f"{dogs = } {dog_form = }")
    return render_template("dashboard/dog.html", dogs=dogs, dog_form=dog_form)


@dog_bp.route("/add", methods=["POST"])
@login_required
@admin_user_required
def add():
    form = DogForm()
    if form.validate_on_submit():
        logger.debug(f"{form.data = }")
        dog = Dog.add(form.data)
        logger.debug(f"{dog = }")
        flash(f"Dog added successfully!", "success")
    return redirect(url_for("dog_bp.get_all"))


@dog_bp.route("/<int:dog_id>", methods=["GET"])
@login_required
def get(dog_id: int):
    dog_form = DogForm()
    dog = dog_service.get_dog(dog_id)
    if dog:
        dog_form.set_data_from_model(dog)
    else:
        flash(f"Dog not found.", "error")
    logger.debug(f"{dog = } {dog_form = }")
    return render_template("dashboard/dog.html", dog=dog, dog_form=dog_form)


@dog_bp.route("/update/<int:dog_id>", methods=["POST", "PUT"])
@login_required
@admin_user_required
def update(dog_id: int):
    dog = Dog.query.get(dog_id)
    form = DogForm()
    if dog and form.validate_on_submit():
        dog.update(form.data)
        flash("Dog updated successfully!", "success")
    else:
        flash("Dog not found.", "error")
    return redirect(url_for("dog_bp.get_all"))


@dog_bp.route("/delete/<int:dog_id>", methods=["POST", "DELETE"])
@login_required
@admin_user_required
def delete(dog_id: int):
    try:
        is_deleted = dog_service.delete_dog(dog_id)
        if is_deleted:
            flash("Dog deleted successfully!", "success")
        else:
            flash("Dog not found.", "error")
    except Exception as e:
        # log the exception
        flash("An error occurred while deleting the dog.", "error")
    return redirect(url_for("dog_bp.get_all"))
