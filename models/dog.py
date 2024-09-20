from app import db
from utils.model_mixin import ModelMixin


class Dog(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    is_allowed_treats = db.Column(db.Boolean, nullable=False)
    is_allowed_off_the_lead = db.Column(db.Boolean, nullable=False)
    is_allowed_on_social_media = db.Column(db.Boolean, nullable=False)
    is_neutered_or_spayed = db.Column(db.Boolean, nullable=False)
    behavioral_issues = db.Column(db.String(6000), nullable=False, default="")
    medical_needs = db.Column(db.String(6000), nullable=False, default="")
    breed = db.Column(db.String(255), nullable=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey("vet.id"), nullable=False)
