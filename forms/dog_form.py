from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    BooleanField,
    DateField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Optional

from models.customer import Customer
from models.dog import Dog
from models.vet import Vet
from utils.form_mixin import FormMixin


class DogForm(FlaskForm, FormMixin):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Scooby Doo"},
    )

    image = FileField(
        "Image",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )

    date_of_birth = DateField(
        "Date of Birth",
        validators=[Optional()],
        render_kw={"placeholder": "YYYY-MM-DD"},
    )

    breed = StringField(
        "Breed", render_kw={"placeholder": "Great Dane"}, validators=[Optional()]
    )

    is_allowed_treats = BooleanField("Allowed Treats", default=False)

    is_allowed_off_the_lead = BooleanField("Allowed Off the Lead", default=False)

    is_allowed_on_social_media = BooleanField("Allowed on Social Media", default=False)

    is_neutered_or_spayed = BooleanField("Neutered/Spayed", default=False)

    behavioral_issues = TextAreaField(
        "Behavioral Issues",
        validators=[Optional()],
        render_kw={
            "placeholder": "Separation anxiety, aggression, etc.",
            "classdss": "u-full-width",
        },
    )

    medical_needs = TextAreaField(
        "Medical Needs",
        validators=[Optional()],
        render_kw={
            "placeholder": "Allergies, medications, etc.",
        },
    )

    customer_id = SelectField("Customer", validators=[DataRequired()], coerce=int)
    vet_id = SelectField("Vet", validators=[DataRequired()], coerce=int)

    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        customer_id_choices = [
            (customer.id, customer.name)
            for customer in Customer.query.order_by(Customer.name).all()
        ]
        self.customer_id.choices = customer_id_choices

        vet_id_choices = [(vet.id, vet.name) for vet in Vet.query.all()]
        self.vet_id.choices = vet_id_choices
