from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy import desc
from forms.customer_form import CustomerForm
from models.customer import Customer
from models.dog import Dog
from models.vet import Vet

customer_bp = Blueprint("customer_bp", __name__)


@customer_bp.route("/", methods=["GET"])
@customer_bp.route("/<int:customer_id>", methods=["GET"])
@login_required
def get(customer_id: int = None):
    customers = None
    customer = None
    customer_form = CustomerForm()
    if customer_id is None:
        customers = Customer.query.order_by(desc(Customer.id)).all()
    else:
        customer = Customer.query.get(customer_id)
        if customer:
            customer_form.set_data_from_model(customer)
        else:
            flash(f"Customer not found.", "error")

    return render_template(
        "admin/customer.html",
        customer=customer,
        customers=customers,
        customer_form=customer_form,
    )


@customer_bp.route("/add", methods=["POST"])
@login_required
def add():
    form = CustomerForm()
    if form.validate_on_submit():
        Customer.add(form.data)
        flash(f"Customer added successfully!", "success")
    return redirect(url_for("customer_bp.get"))


@customer_bp.route("/update/<int:customer_id>", methods=["POST", "PUT"])
@login_required
def update(customer_id: int):
    customer = Customer.query.get(customer_id)
    form = CustomerForm()
    if customer and form.validate_on_submit():
        customer.update(form.data)
        flash("Customer updated successfully!", "success")
    else:
        flash("Customer not found.", "error")
    return redirect(url_for("customer_bp.get"))


@customer_bp.route("/delete/<int:customer_id>", methods=["POST", "DELETE"])
@login_required
def delete(customer_id: int):
    customer = Customer.query.get(customer_id)
    if customer:
        customer.delete()
        flash("Customer deleted successfully!", "success")
    else:
        flash("Customer not found.", "error")
    return redirect(url_for("customer_bp.get"))
