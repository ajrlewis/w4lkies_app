from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional

from utils.form_mixin import FormMixin


class ServiceForm(FlaskForm, FormMixin):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "The name of the service"},
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
        render_kw={"placeholder": "A description of the service"},
    )

    price = DecimalField(
        "Price / £",
        validators=[DataRequired()],
        render_kw={"placeholder": "The price of the service"},
    )

    duration = DecimalField(
        "Duration / minutes",
        validators=[Optional()],
        render_kw={"placeholder": "The duration of the service"},
    )

    is_publicly_offered = BooleanField(
        "Is offered to the public?",
        validators=[Optional()],
        default=False,
    )

    is_active = BooleanField(
        "Is still active?",
        validators=[Optional()],
        default=True,
    )
