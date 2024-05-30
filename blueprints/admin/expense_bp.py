from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from forms.expense_form import ExpenseForm
from models.expense import Expense
from models.expense_type import ExpenseType

expense_bp = Blueprint("expense_bp", __name__)


@expense_bp.route("/", methods=["GET"])
@expense_bp.route("/<int:expense_id>", methods=["GET"])
@login_required
def get(expense_id: int = None):
    expense = None
    expenses = None
    expense_form = ExpenseForm()
    if expense_id is None:
        expenses = Expense.query.order_by(desc(Expense.id)).all()
    else:
        expense = Expense.query.get(expense_id)
        if expense:
            expense_form.set_data_from_model(expense)
        else:
            flash(f"Expense not found.", "error")
    return render_template(
        "admin/expense.html",
        expense=expense,
        expenses=expenses,
        expense_form=expense_form,
    )


@expense_bp.route("/add", methods=["POST"])
@login_required
def add():
    form = ExpenseForm()
    if form.validate_on_submit():
        data = form.data
        data["user_id"] = current_user.id
        Expense.add(data)
        flash(f"Expense added successfully!", "success")
    return redirect(url_for("expense_bp.get"))


@expense_bp.route("/update/<int:expense_id>", methods=["POST", "PUT"])
@login_required
def update(expense_id: int):
    expense = Expense.query.get(expense_id)
    form = ExpenseForm()
    if expense and form.validate_on_submit():
        expense.update(form.data)
        flash("Expense updated successfully!", "success")
    else:
        flash("Expense not found.", "error")
    return redirect(url_for("expense_bp.get"))


@expense_bp.route("/delete/<int:expense_id>", methods=["POST", "DELETE"])
@login_required
def delete(expense_id: int):
    expense = Expense.query.get(expense_id)
    if expense:
        expense.delete()
        flash("Expense deleted successfully!", "success")
    else:
        flash("Expense not found.", "error")
    return redirect(url_for("expense_bp.get"))
