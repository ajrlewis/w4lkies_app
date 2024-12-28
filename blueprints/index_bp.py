from datetime import datetime, timedelta
import os

from flask import current_app, Blueprint, render_template, Response
from flask import Blueprint, render_template
from loguru import logger
from sqlalchemy import desc
from sqlalchemy import desc

from app import db
from models.dog import Dog
from models.service import Service

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/home", methods=["GET"])
def home():
    # Show publicly available services
    # services = (
    #     Service.query.filter_by(is_publicly_offered=True)
    #     .order_by(desc(Service.price))
    #     .all()
    # )
    services = (
        db.session.query(Service)
        .filter_by(is_publicly_offered=True)
        .order_by(desc(Service.price))
        .all()
    )
    logger.debug(f"{services = }")
    return (
        render_template(
            "home.html",
            services=services,
            # dog_name_to_image_paths=dog_name_to_image_paths,
        ),
        200,
    )


@index_bp.route("/", methods=["GET"])
def get():
    # Show publicly available services
    services = (
        Service.query.filter_by(is_publicly_offered=True)
        .order_by(desc(Service.price))
        .all()
    )

    # Show dogs
    dogs = Dog.query.order_by(desc(Dog.id)).all()
    dog_name_to_image_paths = {}
    for dog in dogs:
        key = (dog.name, dog.breed)
        dog_name_to_image_paths[key] = []
        for i in range(2):
            if dog.name.lower() in ["stormi", "simon", "rocky"]:
                image_path = f"img/dogs/{dog.name.lower()}-0{i}.jpg"
                is_file = os.path.isfile(f"static/{image_path}")
                if os.path.isfile(f"static/{image_path}"):
                    dog_name_to_image_paths[key].append(image_path)
        if len(dog_name_to_image_paths[key]) == 0:
            del dog_name_to_image_paths[key]

    # Render template
    return (
        render_template(
            "index.html",
            services=services,
            dog_name_to_image_paths=dog_name_to_image_paths,
        ),
        200,
    )


@index_bp.route("/sitemap.xml")
def sitemap():
    sitemap_xml = render_template("public/sitemap.xml")
    return Response(sitemap_xml, mimetype="text/xml")
