from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from utils.form_mixin import FormMixin
from models.dog_breed import DogBreed


class DogBreedForm(FlaskForm, FormMixin):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Name of the dog breed",
            "class": "u-full-width",
        },
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw={"placeholder": "Description of the breed", "class": "u-full-width"},
    )

    origin = StringField(
        "Origin",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "The country or region where the breed originated.",
            "class": "u-full-width",
        },
    )

    historical_function = TextAreaField(
        "Historical Function",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "The historical function or original purpose for which the breed was bred.",
            "class": "u-full-width",
        },
    )

    life_expectancy = StringField(
        "Life Expectancy in Years",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "The average lifespan of the breed.",
            "class": "u-full-width",
        },
    )

    temperament = StringField(
        "Temperament",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "A description of the typical temperament or personality traits of the breed.",
            "class": "u-full-width",
        },
    )

    walking_duration = StringField(
        "Walking Duration in Minutes",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "The recommended walking duration for the breed.",
            "class": "u-full-width",
        },
    )

    walking_speed = StringField(
        "Walking Speed",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "The recommended walking speed for the breed.",
            "class": "u-full-width",
        },
    )

    common_health_issues = TextAreaField(
        "Common Health Issues",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "A list of common health issues or genetic conditions associated with the breed.",
            "class": "u-full-width",
        },
    )
