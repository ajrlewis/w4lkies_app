from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField
from wtforms.validators import DataRequired
from utils.form_mixin import FormMixin
from models.user import User


class UserForm(FlaskForm, FormMixin):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Dooville Veterinary Hospital",
            "class": "u-full-width",
        },
    )

    address = StringField(
        "Address",
        validators=[DataRequired()],
        render_kw={"placeholder": "Dooville", "class": "u-full-width"},
    )

    phone = TelField(
        "Phone",
        render_kw={"placeholder": "", "class": "u-full-width"},
    )

    submit = SubmitField("Submit")
