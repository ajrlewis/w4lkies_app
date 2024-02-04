from datetime import date
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from models.customer import Customer
from models.invoice import Invoice
from utils.form_mixin import FormMixin


class InvoiceForm(FlaskForm, FormMixin):
    customer_id = SelectField("Customer", coerce=int, validators=[DataRequired()])
    start_date = DateField(
        "Start Date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
    )
    end_date = DateField(
        "End Date", validators=[DataRequired()], format="%Y-%m-%d", default=date.today()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer_id.choices = [
            (customer.id, customer.name) for customer in Customer.query.all()
        ]
