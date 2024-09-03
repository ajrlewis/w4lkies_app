import os

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from loguru import logger
from PIL import Image
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from decorators import admin_user_required
from forms.dog_form import DogForm
from models.dog import Dog
from models.dog_breed import DogBreed

dog_bp = Blueprint("dog_bp", __name__)


@dog_bp.route("/", methods=["GET"])
@dog_bp.route("/<int:dog_id>", methods=["GET"])
@login_required
def get(dog_id: int = None):
    dogs = None
    dog = None
    dog_form = DogForm()
    if dog_id is None:
        dogs = Dog.query.order_by(Dog.name).all()
    else:
        dog = Dog.query.get(dog_id)
        if dog:
            dog_form.set_data_from_model(dog)
        else:
            flash(f"Dog not found.", "error")
    return render_template(
        "dashboard/dog.html",
        dog=dog,
        dogs=dogs,
        dog_form=dog_form,
    )


@dog_bp.route("/add", methods=["POST"])
@login_required
@admin_user_required
def add():
    form = DogForm()
    if form.validate_on_submit():
        dog = Dog.add(form.data)
        logger.debug(f"{dog = }")
        flash(f"Dog added successfully!", "success")
    return redirect(url_for("dog_bp.get"))


@dog_bp.route("/update/<int:dog_id>", methods=["POST", "PUT"])
@login_required
@admin_user_required
def update(dog_id: int):
    dog = Dog.query.get(dog_id)
    form = DogForm()
    if dog and form.validate_on_submit():
        # if form.image.data:
        #     filepath = os.path.join("static/img/dogs", f"{dog.name.lower()}.png")
        #     form.image.data.save(filepath)
        #     process_image(filepath)
        dog.update(form.data)
        flash("Dog updated successfully!", "success")
    else:
        flash("Dog not found.", "error")
    return redirect(url_for("dog_bp.get"))


# def process_image(filepath):
#     image = Image.open(filepath)
#     if image.format != "PNG":
#         image = image.convert("RGBA")
#         image.save(filepath, "PNG")
#     image.save(filepath, optimize=True, quality=85)


@dog_bp.route("/delete/<int:dog_id>", methods=["POST", "DELETE"])
@login_required
@admin_user_required
def delete(dog_id: int):
    dog = Dog.query.get(dog_id)
    if dog:
        dog.delete()
        flash("Dog deleted successfully!", "success")
    else:
        flash("Dog not found.", "error")
    return redirect(url_for("dog_bp.get"))
