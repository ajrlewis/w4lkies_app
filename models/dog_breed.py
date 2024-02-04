from app import db
from utils.model_mixin import ModelMixin


class DogBreed(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # The name of the dog breed.
    name = db.Column(db.String(255), nullable=False)

    # The description of the breed
    description = db.Column(db.String(255), nullable=True)

    # The country or region where the breed originated.
    origin = db.Column(db.String(255), nullable=True)

    # The historical function or original purpose for which the breed was bred.
    historical_function = db.Column(db.String(255), nullable=True)

    # The average lifespan of the breed.
    life_expectancy = db.Column(db.String(255), nullable=True)

    # A description of the typical temperament or personality traits of the breed.
    temperament = db.Column(db.String(255), nullable=True)

    # The recommended walking duration for the breed.
    walking_duration = db.Column(db.String(255), nullable=True)

    # The recommended walking speed for the breed.
    walking_speed = db.Column(db.String(255), nullable=True)

    # A list of common health issues or genetic conditions associated with the breed.
    common_health_issues = db.Column(db.String(255), nullable=True)
