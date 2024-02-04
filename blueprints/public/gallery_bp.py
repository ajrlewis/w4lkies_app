import os
from flask import Blueprint, render_template
from sqlalchemy import desc
from models.dog import Dog
from models.dog_breed import DogBreed

gallery_bp = Blueprint("gallery_bp", __name__)


@gallery_bp.route("/", methods=["GET"])
def get():
    dogs = Dog.query.join(DogBreed).order_by(desc(Dog.id)).all()
    dog_name_to_image_paths = {}
    for dog in dogs:
        key = (dog.name, dog.dog_breed.name)
        dog_name_to_image_paths[key] = []
        # for i in range(10):
        for i in range(2):
            image_path = f"img/dogs/{dog.name.lower()}-0{i}.jpg"
            is_file = os.path.isfile(f"static/{image_path}")
            if os.path.isfile(f"static/{image_path}"):
                dog_name_to_image_paths[key].append(image_path)
        if len(dog_name_to_image_paths[key]) == 0:
            del dog_name_to_image_paths[key]
    return (
        render_template(
            "public/gallery.html", dog_name_to_image_paths=dog_name_to_image_paths
        ),
        200,
    )
