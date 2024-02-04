from app import db
from utils.model_mixin import ModelMixin


class Invoice(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    date_issued = db.Column(db.Date, nullable=False)
    bookings = db.relationship("Booking", backref="invoice")
    subtotal_price = db.Column(db.Float, nullable=False)
    total_price_discount = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False, default=False)
