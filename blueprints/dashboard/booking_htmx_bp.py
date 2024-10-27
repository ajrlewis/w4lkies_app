from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required
from loguru import logger

from app import db
from decorators import admin_user_required
from services import booking_service, user_service

booking_htmx_bp = Blueprint("booking_htmx_bp", __name__)


def render_oob_template(
    template: str, div_id: str, hx_swap_oob: str = "outerHTML", **kwargs
) -> str:
    rendered_template = render_template(template, **kwargs)
    rendered_oob_template = (
        f'<div id="{div_id}" hx-swap-oob="{hx_swap_oob}">{rendered_template}</div>'
    )
    return rendered_oob_template


@booking_htmx_bp.route("", methods=["GET"])
@login_required
def get_base():
    booking_form = booking_service.get_form()
    booking_filter_form = booking_service.get_filter_form()
    if current_user.is_admin:
        bookings = booking_service.get_all()
    else:
        bookings = booking_service.get_all(user_id=current_user.id)
    return render_template(
        "dashboard/bookings_base.html",
        booking_form=booking_form,
        booking_filter_form=booking_filter_form,
        bookings=bookings,
    )


@booking_htmx_bp.route("/<int:booking_id>", methods=["GET"])
@login_required
def get(booking_id: int):
    booking = booking_service.get(booking_id=booking_id)
    return render_template("dashboard/booking_detail.html", booking=booking)


# @booking_htmx_bp.route("/all", methods=["GET"])
# @login_required
# def get_all():
#     bookings = booking_service.get_all()
#     return render_template("dashboard/bookings.html", bookings=bookings)


@booking_htmx_bp.route("/filter", methods=["POST"])
@login_required
def get_filtered():
    booking_filter_form = booking_service.get_filter_form()
    data = booking_filter_form.data
    if not current_user.is_admin:
        data["user_id"] = current_user.id
    logger.debug(f"{data = }")
    bookings = booking_service.get_all(
        user_id=data.get("user_id"),
        date_min=data.get("date_min"),
        date_max=data.get("date_max"),
    )
    return render_template("dashboard/bookings.html", bookings=bookings)


@booking_htmx_bp.route("/summary", methods=["GET"])
@login_required
def summary():
    booking = booking_service.get(booking_id)
    booking_form = booking_service.get_form()
    logger.debug(f"{booking = } {booking_form = }")
    if booking and booking_form.validate_on_submit():
        logger.debug(f"{booking_form.data = }")
        booking = booking_service.update(booking_id, booking_form.data)
        bookings = booking_service.get_all()
        logger.debug(f"{bookings = }")
    return render_template("dashboard/bookings.html", bookings=bookings)


@booking_htmx_bp.route("/", methods=["POST"])
@login_required
def add():
    booking_form = booking_service.get_form()
    if booking_form.validate_on_submit():
        data = booking_form.data
        repeat_weeks = data.get("repeat_weeks", 0)
        booking_service.add(data)

        bookings = booking_service.get_all()
        logger.debug(f"{bookings = }")
        template = render_oob_template(
            "dashboard/bookings.html",
            div_id="bookings",
            hx_swap_oob="outerHTML",
            bookings=bookings,
        )

        first_booking = bookings[-1]
        logger.debug(f"{first_booking = }")
        booking_form = booking_service.get_form(first_booking)
        # booking_form.
        template = (
            render_template("dashboard/booking_form.html", booking_form=booking_form)
            + template
        )
        # flash(f"Booking added successfully!", "success")

    else:
        logger.error("booking form did not validate on submit")
        return ""

    # test_template = render_template("dashboard/test.html", test="Foo")
    # template += (
    #     '\n\n<div id="test" hx-swap-oob="outerHTML">\n' + test_template + "\n</div>"
    # )
    return template


@booking_htmx_bp.route("/<int:booking_id>/edit", methods=["GET"])
@login_required
def edit(booking_id: int):
    booking = booking_service.get(booking_id)
    booking_form = booking_service.get_form(booking)
    return render_template(
        "dashboard/booking_edit.html", booking=booking, booking_form=booking_form
    )


@booking_htmx_bp.route("/<int:booking_id>", methods=["PUT"])
@login_required
def update(booking_id: int):
    booking = booking_service.get(booking_id)
    booking_form = booking_service.get_form()
    logger.debug(f"{booking = } {booking_form = }")
    if booking and booking_form.validate_on_submit():
        logger.debug(f"{booking_form.data = }")
        booking = booking_service.update(booking_id, booking_form.data)
        if current_user.is_admin:
            bookings = booking_service.get_all()
        else:
            bookings = booking_service.get_all(user_id=current_user.id)
        logger.debug(f"{bookings = }")
    return render_template("dashboard/bookings.html", bookings=bookings)


@booking_htmx_bp.route("/<int:booking_id>", methods=["DELETE"])
@login_required
def delete(booking_id: int):
    logger.debug(f"{booking_id = }")
    booking_service.delete(booking_id)
    flash(f"Deleted {booking_id = }!", "success")
    return ""
