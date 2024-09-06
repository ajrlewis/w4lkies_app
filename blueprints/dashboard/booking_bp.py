import calendar
from datetime import date, timedelta

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from loguru import logger
import pandas as pd
from sqlalchemy import desc

from decorators import admin_user_required
from forms.booking_form import BookingForm
from models.booking import Booking
from models.customer import Customer
from models.dog import Dog

booking_bp = Blueprint("booking_bp", __name__)


@booking_bp.route("", methods=["GET"])
@booking_bp.route("/", methods=["GET"])
@booking_bp.route("/<int:booking_id>", methods=["GET"])
@login_required
def get(booking_id: int = None):
    booking = None
    previous_bookings = None
    upcoming_bookings = None
    summary_bookings = None
    form = BookingForm()
    if booking_id is None:
        # Get all bookings
        query = Booking.query
        if not current_user.is_admin:
            logger.debug("Current user is not admin, querying only bookings for user.")
            query = query.filter_by(user_id=current_user.id)
        bookings = query.order_by(desc(Booking.id)).all()

        # Compute summary of bookings for admin user
        if current_user.is_admin:
            summary_data = [
                {
                    "user_name": b.user.name,
                    "booking_year": b.date.year,
                    "booking_month_number": b.date.month,
                    "booking_month": b.date.strftime("%b"),
                    "booking_price": b.service.price,
                }
                for b in bookings
                if b.service.price > 10.0  # don't include add-ons
                # and b.date >  # only include past 3 months
            ]
            summary_df = pd.DataFrame(summary_data)
            summary_gb = summary_df.groupby(
                ["user_name", "booking_year", "booking_month_number"]
            )
            summary_df = summary_gb.agg(
                booking_month=("booking_month", min),
                number_of_bookings=("booking_price", len),
                total_price_of_bookings=("booking_price", sum),
            ).reset_index()
            summary_df = summary_df.drop(columns="booking_month_number")
            logger.debug(summary_df)

            summary_bookings = (
                summary_df.groupby("user_name")
                .apply(
                    lambda s: s[
                        [
                            "booking_year",
                            "booking_month",
                            "number_of_bookings",
                            "total_price_of_bookings",
                        ]
                    ].to_dict(orient="records")
                )
                .to_dict()
            )
            logger.debug(summary_bookings)

        logger.debug(f"{len(bookings) = })")
        if bookings:
            logger.debug(f"Found {len(bookings) = }")
            # Set form data to last booking's values for UX improvement
            form.set_data_from_model(bookings[0])

            # Separate previous and upcoming bookings
            today = date.today()
            previous_bookings = []
            upcoming_bookings = {}
            for b in bookings:
                booking_date = b.date
                if booking_date >= today:
                    day_of_week = calendar.day_abbr[booking_date.weekday()]
                    key = (booking_date, day_of_week)
                    if key in upcoming_bookings:
                        upcoming_bookings[key].append(b)
                    else:
                        upcoming_bookings[key] = [b]
                else:
                    previous_bookings.append(b)

            # Sort upcoming bookings by descending key and ascending values
            upcoming_bookings = dict(sorted(upcoming_bookings.items()))
            for k, values in upcoming_bookings.items():
                upcoming_bookings[k] = sorted(
                    upcoming_bookings[k], key=lambda b: b.time
                )

    else:
        # Return details for specified booking
        booking = Booking.query.get(booking_id)
        logger.debug(f"{booking = }")
        if booking:
            form.set_data_from_model(booking)
            form.time.data = booking.time.strftime("%H:%M:%S")
        else:
            flash(f"Booking not found.", "error")

    return render_template(
        "dashboard/booking.html",
        booking=booking,
        upcoming_bookings=upcoming_bookings,
        previous_bookings=previous_bookings,
        summary_bookings=summary_bookings,
        form=form,
    )


@booking_bp.route("/add", methods=["POST"])
@login_required
@admin_user_required
def add():
    form = BookingForm()
    if current_user.is_admin and form.validate_on_submit():
        data = form.data
        booking = Booking.add(data)
        logger.debug(f"Added {booking = }")
        flash(f"Booking added successfully!", "success")
    return redirect(url_for("booking_bp.get"))


@booking_bp.route("/update/<int:booking_id>", methods=["POST", "PUT"])
@login_required
@admin_user_required
def update(booking_id: int):
    booking = Booking.query.get(booking_id)
    logger.debug(f"{booking = }")
    form = BookingForm()
    if booking and form.validate_on_submit():
        form_data = form.data
        logger.debug(f"{form_data = }")
        booking.update(form_data)
        flash("Booking updated successfully!", "success")
    else:
        flash("Booking not found.", "error")
    return redirect(url_for("booking_bp.get"))


@booking_bp.route("/delete/<int:booking_id>", methods=["POST", "DELETE"])
@login_required
@admin_user_required
def delete(booking_id: int):
    booking = Booking.query.get(booking_id)
    if booking:
        booking.delete()
        flash("Booking deleted successfully!", "success")
    else:
        flash("Booking not found.", "error")
    return redirect(url_for("booking_bp.get"))
