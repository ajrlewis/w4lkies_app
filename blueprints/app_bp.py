from flask import Blueprint, render_template, send_from_directory
from loguru import logger

app_bp = Blueprint("app_bp", __name__)


def htmx_oob_render_template(
    template: str, div_id: str, hx_swap_oob: str = "outerHTML", **kwargs
) -> str:
    logger.debug(f"{div_id = } {hx_swap_oob = }")
    rendered_template = render_template(template, **kwargs)
    rendered_oob_template = (
        f'<div id="{div_id}" hx-swap-oob="{hx_swap_oob}">{rendered_template}</div>'
    )
    return rendered_oob_template


# Customers

from flask_login import login_required
from loguru import logger

from services import customer_service


@app_bp.route("/customers/", methods=["GET"])
@login_required
def get_customers():
    customers = customer_service.get_customers()
    logger.debug(f"{customers = }")
    return render_template("customers.html", customers=customers)


@app_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id: int):
    logger.debug(f"{customer_id = }")
    customer = customer_service.get_customer(customer_id)
    logger.debug(f"{customer = }")
    return render_template("customer_detail.html", customer=customer)


# Users

from flask_login import login_required
from loguru import logger

from services import user_service


@app_bp.route("/users/", methods=["GET"])
@login_required
def get_users():
    users = user_service.get_users()
    user_form = user_service.get_user_form()
    logger.debug(f"{users = } {user_form = }")
    return render_template("app/users.html", users=users, user_form=user_form)


@app_bp.route("/users/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id: int):
    logger.debug(f"{user_id = }")
    user = user_service.get_user_by_id(user_id)
    logger.debug(f"{user = }")
    return render_template("app/user_detail.html", user=user)


@app_bp.route("/users/<int:user_id>/edit", methods=["GET"])
@login_required
def edit_user(user_id: int):
    logger.debug(f"{user_id = }")
    user = user_service.get_user_by_id(user_id)
    logger.debug(f"{user = }")
    user_form = user_service.get_user_form(user)
    logger.debug(f"{user_form = }")
    return render_template("app/user_edit.html", user=user, user_form=user_form)


@app_bp.route("/users/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id: int):
    logger.debug(f"{user_id = }")
    user_form = user_service.get_user_form()
    logger.debug(f"{user_form = }")
    if user_form.validate_on_submit():
        user_data = user_form.data
        logger.debug(f"{user_data = }")
        user = user_service.update_user_by_id(user_id, user_data)
        logger.debug(f"{user = }")
        return render_template("app/user_detail.html", user=user)
    else:
        logger.error("User form did not validate on submit")
        return ""


@app_bp.route("/users/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id: int):
    logger.debug(f"{user_id = }")
    user_service.delete_user_by_id(user_id)
    return ""


@app_bp.route("/users/add", methods=["GET"])
def add_user_form():
    user_form = user_service.get_user_form()
    return render_template("app/user_form.html", user_form=user_form)


@app_bp.route("/users", methods=["POST"])
@login_required
def add_user():
    # Add new user
    user_form = user_service.get_user_form()
    if user_form.validate_on_submit():
        user_data = user_form.data
        logger.debug(f"{user_data = }")
        user = user_service.add_user(user_data=user_data)
        logger.debug(f"{user = }")

    # Reset form and get latest users
    users = user_service.get_users()
    logger.debug(f"{users = }")
    user_form = user_service.get_user_form()
    logger.debug(f"{user_form = }")
    return render_template("app/users.html", users=users, user_form=user_form)


# App


@app_bp.route("/")
def index():
    return render_template("app/app.html")
