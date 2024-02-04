from app import db
from utils.model_mixin import ModelMixin
from models.expense_type import ExpenseType


class Expense(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    expense_type_id = db.Column(
        db.Integer, db.ForeignKey("expense_type.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
