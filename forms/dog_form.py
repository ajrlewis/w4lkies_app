from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Optional
from utils.form_mixin import FormMixin
from models.customer import Customer
from models.dog_breed import DogBreed
from models.vet import Vet


class DogForm(FlaskForm, FormMixin):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Scooby Doo", "class": "u-full-width"},
    )

    date_of_birth = DateField(
        "Date of Birth",
        validators=[Optional()],
        # default=datetime.utcnow,
        render_kw={"placeholder": "YYYY-MM-DD", "class": "u-full-width"},
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
            "class": "u-full-width",
        },
    )

    dog_breed_id = SelectField(
        "Breed",
        default="Great Dane",
        validators=[DataRequired()],
    )
    customer_id = SelectField("Customer", validators=[DataRequired()])
    vet_id = SelectField("Vet", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # sql = """
        # SELECT name FROM DogBreed ORDER BY name ASC
        # """
        dog_breed_id_choices = [
            (breed.id, breed.name)
            for breed in DogBreed.query.order_by(DogBreed.name).all()
        ]
        self.dog_breed_id.choices = dog_breed_id_choices

        customer_id_choices = [
            (customer.id, customer.name)
            for customer in Customer.query.order_by(Customer.name).all()
        ]
        self.customer_id.choices = customer_id_choices

        vet_id_choices = [(vet.id, vet.name) for vet in Vet.query.all()]
        self.vet_id.choices = vet_id_choices
