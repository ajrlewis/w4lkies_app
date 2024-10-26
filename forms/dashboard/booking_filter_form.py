from datetime import date, datetime, timedelta, time

from flask_wtf import FlaskForm
from loguru import logger

from wtforms import (
    BooleanField,
    DateField,
    IntegerField,
    SelectField,
    SubmitField,
)

# from wtforms.fields import DateField
from wtforms.validators import DataRequired, Optional

from models.customer import Customer
from models.service import Service
from models.user import User
from utils.form_mixin import FormMixin


class BookingFilterForm(FlaskForm, FormMixin):
    user_id = SelectField("Filter by user", coerce=int, validators=[Optional()])
    date_min = DateField(
        "From this date",
        validators=[Optional()],
        format="%Y-%m-%d",
        render_kw={"placeholder": "yyyy-mm-dd"},
    )
    date_max = DateField(
        "Up to and including this date",
        validators=[Optional()],
        format="%Y-%m-%d",
        render_kw={"placeholder": "yyyy-mm-dd"},
    )
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_id_choices = [(-1, "All Users")] + [
            (user.id, user.name) for user in User.query.order_by(User.name).all()
        ]
        self.user_id.choices = user_id_choices
