from datetime import date
from flask_wtf import FlaskForm
from wtforms.fields import (
    DateField,
    DecimalField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Optional
from utils.form_mixin import FormMixin
from models.expense_type import ExpenseType


class ExpenseForm(FlaskForm, FormMixin):
    date = DateField(
        "Date", validators=[DataRequired()], format="%Y-%m-%d", default=date.today()
    )
    expense_type_name = SelectField("Type", validators=[DataRequired()])
    # Marketing, Poo Bags, Toys, Treats, Insurance, Website, Miscellaneous,
    price = DecimalField("Price", validators=[DataRequired()])
    comment = StringField("Comment", validators=[Optional()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        expense_type_names = [
            expense_type.name
            for expense_type in ExpenseType.query.order_by(ExpenseType.name).all()
        ]
        self.expense_type_name.choices = expense_type_names
