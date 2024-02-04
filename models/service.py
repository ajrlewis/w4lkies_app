from app import db
from utils.model_mixin import ModelMixin


class Service(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), default="", nullable=False)
    duration = db.Column(db.Float, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
