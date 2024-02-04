import json
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import desc
from models.customer import Customer
from models.dog import Dog
from models.dog_breed import DogBreed
from models.vet import Vet

verify_sign_up_bp = Blueprint("verify_sign_up_bp", __name__)


@verify_sign_up_bp.route("/", methods=["GET"])
@login_required
def get():
    return render_template("admin/verify_sign_up.html")


def extract_data(data: dict[str, str], prefix: str):
    data = {
        f"{k.replace(prefix, '')}": v for k, v in data.items() if k.startswith(prefix)
    }
    return data


# TODO (ajrl) Add try-except clauses.
@verify_sign_up_bp.route("/add", methods=["POST"])
@login_required
def add():
    json_data = request.form.get("json_data")
    data = json.loads(json_data)
    data = {k: v for k, v in data.items() if v != "N/A"}

    # 1. Add the customer
    customer_data = extract_data(data, "customer_")
    customer = Customer.query.filter_by(name=customer_data["name"]).first()
    if not customer:
        customer = Customer.add(customer_data)

    # 2. Get or add the vet
    vet_data = extract_data(data, "vet_")
    vet = Vet.query.filter_by(name=vet_data["name"]).first()
    if not vet:
        vet_data = {"name": vet_data["name"], "address": "", "phone": ""}
        vet = Vet.add(vet_data)

    # 3. Add dog_breed
    dog_breed_data = extract_data(data, "dog_breed_")
    dog_breed = DogBreed.query.filter_by(name=dog_breed_data["name"]).first()
    if not dog_breed:
        dog_breed_data = {
            "name": dog_breed_data["name"],
            "description": "",
            "origin": "",
            "historical_function": "",
            "life_expectancy": "",
            "temperament": "",
            "walking_duration": "",
            "walking_speed": "",
            "common_health_issues": "",
        }
        dog_breed = DogBreed.add(dog_breed_data)

    # 4. Add dog
    dog_prefix = "dog_"
    dog_data = {
        f"{k.replace(dog_prefix, '')}": v
        for k, v in data.items()
        if k.startswith(dog_prefix)
    }
    dog = Dog.query.filter_by(name=dog_data["name"]).first()
    if not dog:
        dog_data["dog_breed_id"] = dog_breed.id
        dog_data["customer_id"] = customer.id
        dog_data["vet_id"] = vet.id
        dog = Dog.add(dog_data)

    flash("Sign up added successfully!", "success")
    return redirect(url_for("verify_sign_up_bp.get"))
