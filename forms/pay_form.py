from bitcoinkit.bitcoin_price import VALID_CURRENCIES
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired


class PayForm(FlaskForm):
    currency = SelectField(
        "Currency",
        validators=[DataRequired()],
        choices=[(c, c) for c in VALID_CURRENCIES + ["BTC", "satoshi"]],
    )
    amount = DecimalField("Amount", validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Generate Invoice")
