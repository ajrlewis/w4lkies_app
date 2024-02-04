from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from forms.dog_breed_form import DogBreedForm
from models.dog_breed import DogBreed

dog_breed_bp = Blueprint("dog_breed_bp", __name__)


@dog_breed_bp.route("/", methods=["GET"])
@dog_breed_bp.route("/<int:dog_breed_id>", methods=["GET"])
@login_required
def get(dog_breed_id: int = None):
    dog_breeds = None
    dog_breed = None
    dog_breed_form = DogBreedForm()
    if dog_breed_id is None:
        dog_breeds = DogBreed.query.order_by(DogBreed.name).all()
    else:
        dog_breed = DogBreed.query.get(dog_breed_id)
        if dog_breed:
            dog_breed_form.set_data_from_model(dog_breed)
        else:
            flash(f"Dog breed not found.", "error")
    return render_template(
        "admin/dog_breed.html",
        dog_breed=dog_breed,
        dog_breeds=dog_breeds,
        dog_breed_form=dog_breed_form,
    )


@dog_breed_bp.route("/add", methods=["POST"])
@login_required
def add():
    form = DogBreedForm()
    if form.validate_on_submit():
        DogBreed.add(form.data)
        flash(f"Dog breed added successfully!", "success")
    else:
        flash(f"Dog breed not added!", "error")
    return redirect(url_for("dog_breed_bp.get"))


@dog_breed_bp.route("/update/<int:dog_breed_id>", methods=["POST", "PUT"])
@login_required
def update(dog_breed_id: int):
    dog_breed = DogBreed.query.get(dog_breed_id)
    form = DogBreedForm()
    if dog_breed and form.validate_on_submit():
        dog_breed.update(form.data)
        flash("Dog breed updated successfully!", "success")
    else:
        flash("Dog breed not found.", "error")
    return redirect(url_for("dog_breed_bp.get"))


@dog_breed_bp.route("/delete/<int:dog_breed_id>", methods=["POST", "DELETE"])
@login_required
def delete(dog_breed_id: int):
    dog_breed = DogBreed.query.get(dog_breed_id)
    if dog_breed:
        dog_breed.delete()
        flash("Dog breed deleted successfully!", "success")
    else:
        flash("Dog breed not found.", "error")
    return redirect(url_for("dog_breed_bp.get"))
