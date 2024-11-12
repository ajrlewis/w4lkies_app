from app import db
from utils.model_mixin import ModelMixin


class Customer(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    emergency_contact_name = db.Column(db.String(255), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)
    dogs = db.relationship("Dog", backref="customer", lazy=True)
    signed_up_on = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    __table_args__ = (db.UniqueConstraint("name", "email"),)

    def __repr__(self):
        return f"<Customer {self.id}>"
