from app import db
from utils.model_mixin import ModelMixin


class Booking(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    customer = db.relationship("Customer", backref="booking")

    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    service = db.relationship("Service", backref="booking")

    invoice_id = db.Column(db.Integer, db.ForeignKey("invoice.id"), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    user = db.relationship("User", backref="booking", foreign_keys=[user_id])

    def to_dict(self) -> dict:
        return {
            "booking_id": self.id,
            "date": f"{self.date}",
            "time": f"{self.time}",
            "customer_name": self.customer.name,
            "service_name": self.service.name,
            "user_name": self.user.name,
        }
