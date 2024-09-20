from datetime import datetime
from typing import Any, Dict

from flask import render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    BooleanField,
    DateField,
    SelectField,
    SubmitField,
    StringField,
    TelField,
    TextAreaField,
)
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired, Optional

from models.dog import Dog
from models.vet import Vet
from utils.form_mixin import FormMixin


class SignUpForm(FlaskForm, FormMixin):
    customer_name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Daphne Blake", "class": "u-full-width"},
    )

    customer_phone = TelField(
        "Phone",
        validators=[DataRequired()],
        render_kw={"placeholder": "(+44) 0123 456789", "class": "u-full-width"},
    )

    customer_email = StringField(
        "Email",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "daphne@themysterymachine.com",
            "class": "u-full-width",
        },
    )

    customer_emergency_contact_name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Fred Jones", "class": "u-full-width"},
    )

    customer_emergency_contact_phone = TelField(
        "Phone",
        validators=[DataRequired()],
        render_kw={"placeholder": "(+44) 1234 567890", "class": "u-full-width"},
    )

    customer_signed_up_on = DateField("customer_signed_up_on", default=datetime.utcnow)

    vet_name = SelectField(
        "Vet",
        default="Dooville Veterinary Hospital",
        validators=[DataRequired()],
        render_kw={"placeholder": "Doo", "class": "u-full-width"},
    )

    other_vet_name = StringField("Other Vet")

    dog_name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Scooby Doo", "class": "u-full-width"},
    )

    dog_breed = SelectField(
        "Breed",
        default="Great Dane",
        validators=[DataRequired()],
        render_kw={"placeholder": "Great Dane", "class": "u-full-width"},
    )
    other_dog_breed = StringField(
        "Other Dog Breed",
        render_kw={
            "placeholder": "Enter other dog breed",
            "class": "u-full-width",
        },
    )

    dog_date_of_birth = DateField(
        "Date of Birth",
        validators=[Optional()],
        render_kw={"class": "u-full-width"},
    )

    dog_is_allowed_treats = BooleanField(
        "Allowed treats?",
        default=False,
    )

    dog_is_allowed_off_the_lead = BooleanField(
        "Allowed off the lead?",
        default=False,
    )

    dog_is_allowed_on_social_media = BooleanField(
        "Allowed on Instagram (@w4lkies) or this website (w4lkies.com)?",
        default=False,
    )

    dog_is_neutered_or_spayed = BooleanField("Neutered or spayed?", default=False)

    dog_behavioral_issues = TextAreaField(
        "Behavioral Issues",
        validators=[Optional()],
        render_kw={
            "placeholder": "Enter any behavior issues your dog may have",
            "class": "u-full-width",
        },
    )

    dog_medical_needs = TextAreaField(
        "Medical Needs / Allergies",
        validators=[Optional()],
        render_kw={
            "placeholder": "Enter any information about your dog's medical needs or allergies",
            "class": "u-full-width",
        },
    )

    consent = BooleanField(
        f"""
        "I authorize W4lkies to care for my dog(s) in my absence and to transport them to a veterinary clinic for medical treatment if necessary. I understand that I will be responsible for payment for any treatment provided to my dog(s) by W4lkies or the veterinary clinic. In the event that W4lkies is unable to contact me or my emergency contact, I authorize W4lkies and the veterinary clinic to make any necessary decisions regarding my dog(s) medical treatment."
        """,
        validators=[DataRequired()],
    )

    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        vet_names = [vet.name for vet in Vet.query.order_by(Vet.name).all()]
        vet_names = ["Dooville Veterinary Hospital"] + vet_names + ["Other"]
        self.vet_name.choices = vet_names

        dog_breeds = [dog.breed for dog in Dog.query.all()]
        dog_breeds = sorted(list(set(dog_breeds)))
        dog_breeds = list(set(dog_breeds))
        dog_breeds = ["Great Dane"] + dog_breeds + ["Other"]
        self.dog_breed.choices = dog_breeds

    def to_dict(self) -> Dict[str, Any]:
        customer_signed_up_on = self.customer_signed_up_on.data.strftime("%Y-%m-%d")
        customer_name = self.customer_name.data
        customer_phone = self.customer_phone.data
        customer_email = self.customer_email.data
        customer_emergency_contact_name = self.customer_emergency_contact_name.data
        customer_emergency_contact_phone = self.customer_emergency_contact_phone.data
        vet_name = self.vet_name.data
        if vet_name == "Other":
            vet_name = self.other_vet_name.data
        dog_name = self.dog_name.data
        dog_breed = self.dog_breed.data
        if dog_breed == "Other":
            dog_breed = self.other_dog_breed.data
        dog_date_of_birth = self.dog_date_of_birth.data
        if dog_date_of_birth:
            dog_date_of_birth = dog_date_of_birth.strftime("%Y-%m-%d")
        else:
            dog_date_of_birth = "N/A"
        dog_is_allowed_treats = self.dog_is_allowed_treats.data
        dog_is_allowed_off_the_lead = self.dog_is_allowed_off_the_lead.data
        dog_is_allowed_on_social_media = self.dog_is_allowed_on_social_media.data
        dog_is_allowed_treats = self.dog_is_allowed_treats.data
        dog_is_neutered_or_spayed = self.dog_is_neutered_or_spayed.data
        dog_behavioral_issues = self.dog_behavioral_issues.data.strip()
        if not dog_behavioral_issues:
            dog_behavioral_issues = "N/A"
        dog_medical_needs = self.dog_medical_needs.data.strip()
        if not dog_medical_needs:
            dog_medical_needs = "N/A"
        data = {
            "customer_signed_up_on": customer_signed_up_on,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_email": customer_email,
            "customer_emergency_contact_name": customer_emergency_contact_name,
            "customer_emergency_contact_phone": customer_emergency_contact_phone,
            "vet_name": vet_name,
            "dog_name": dog_name,
            "dog_breed": dog_breed,
            "dog_date_of_birth": dog_date_of_birth,
            "dog_is_allowed_treats": dog_is_allowed_treats,
            "dog_is_allowed_off_the_lead": dog_is_allowed_off_the_lead,
            "dog_is_allowed_on_social_media": dog_is_allowed_on_social_media,
            "dog_is_allowed_treats": dog_is_allowed_treats,
            "dog_is_neutered_or_spayed": dog_is_neutered_or_spayed,
            "dog_behavioral_issues": dog_behavioral_issues,
            "dog_medical_needs": dog_medical_needs,
        }
        return data
