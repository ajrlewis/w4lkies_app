from app import db
from utils.model_mixin import ModelMixin


class ExpenseType(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    expenses = db.relationship("Expense", backref="expense_type", lazy=True)
