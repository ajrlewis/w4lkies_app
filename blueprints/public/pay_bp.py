from datetime import date
from bitcoinkit import bitcoin_price, bitcoin_units
from flask import Blueprint, jsonify, render_template
from app import wos
from forms.pay_form import PayForm

pay_bp = Blueprint("pay_bp", __name__)


@pay_bp.route("/", methods=["GET"])
def get():
    form = PayForm()
    return render_template("public/pay.html", form=form)


@pay_bp.route("/lnurl/pay", methods=["POST"])
def get_invoice():
    form = PayForm()
    if form.validate_on_submit():
        currency = form.currency.data
        amount = form.amount.data

        date_str = date.today().strftime("%Y-%m-%d")
        amount_str = f"{currency} {amount:,.2f}"

        # 1. Convert amount from currency to BTC
        if currency == "GBP":
            amount /= bitcoin_price.gbp()
        elif currency == "EUR":
            amount /= bitcoin_price.eur()
        elif currency == "USD":
            amount /= bitcoin_price.usd()
        elif currency == "satoshi":
            amount = bitcoin_units.satoshis_to_bitcoins(amount)

        # 2. Convert BTC amount to milli Satoshis
        amount = bitcoin_units.bitcoins_to_satoshis(amount)
        amount = bitcoin_units.satoshis_to_millisatoshis(amount)

        # 3. Create Lightning invoice
        data = wos._wallet.pay_request(amount=amount)

        return (
            jsonify({"date": date_str, "amount": amount_str, "pr": data["pr"]}),
            200,
        )
    else:
        return jsonify({"error": "Invalid input data"}), 400
