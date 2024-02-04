from app import db
from utils.model_mixin import ModelMixin


class Vet(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    dogs = db.relationship("Dog", backref="vet", lazy=True)
