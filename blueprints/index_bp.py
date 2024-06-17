from datetime import datetime, timedelta
from flask import current_app, Blueprint, render_template, Response
from sqlalchemy import desc
from models.service import Service

import os
from flask import Blueprint, render_template
from sqlalchemy import desc
from models.dog import Dog
from models.dog_breed import DogBreed

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/", methods=["GET"])
def get():
    services = (
        Service.query.filter_by(is_publicly_offered=True)
        .order_by(desc(Service.price))
        .all()
    )

    dogs = Dog.query.join(DogBreed).order_by(desc(Dog.id)).all()
    dog_name_to_image_paths = {}
    for dog in dogs:
        key = (dog.name, dog.dog_breed.name)
        dog_name_to_image_paths[key] = []
        # for i in range(10):
        for i in range(2):
            if dog.name.lower() in ["stormi", "simon", "rocky"]:
                image_path = f"img/dogs/{dog.name.lower()}-0{i}.jpg"
                is_file = os.path.isfile(f"static/{image_path}")
                if os.path.isfile(f"static/{image_path}"):
                    dog_name_to_image_paths[key].append(image_path)
        if len(dog_name_to_image_paths[key]) == 0:
            del dog_name_to_image_paths[key]

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
    # pages = []
    # lastmod = datetime.now() - timedelta(days=10)
    # for rule in current_app.url_map.iter_rules():
    #     if "GET" in rule.methods:
    #         exclude_urls = ["/admin/", "/static"]
    #         url = rule.rule
    #         page = {"url": url, "lastmod": lastmod.strftime("%Y-%m-%d")}
    #         if not any(exclude_url in url for exclude_url in exclude_urls):
    #             pages.append(page)
    # sitemap_xml = render_template("public/sitemap.xml", pages=pages)
    sitemap_xml = render_template("public/sitemap.xml")
    return Response(sitemap_xml, mimetype="text/xml")
