import calendar
from datetime import date, timedelta
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from forms.booking_form import BookingForm
from models.booking import Booking
from models.customer import Customer
from models.dog import Dog

booking_bp = Blueprint("booking_bp", __name__)


# TODO (ajrl) This is really bad! Make different methods to get past and upcoming bookings.
@booking_bp.route("/", methods=["GET"])
@booking_bp.route("/<int:booking_id>", methods=["GET"])
@login_required
def get(booking_id: int = None):
    booking = None
    previous_bookings = None
    upcoming_bookings = None
    form = BookingForm()
    if booking_id is None:
        # Get all bookings
        bookings = (
            Booking.query.filter_by(user_id=current_user.id)
            .order_by(desc(Booking.id))
            .all()
        )
        if bookings:
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
            new_keys = []
            for k, values in upcoming_bookings.items():
                upcoming_bookings[k] = sorted(
                    upcoming_bookings[k], key=lambda b: b.time
                )
                # Remove duplicate bookings at the same time
                number_of_bookings = len(set([v.time for v in values]))
                total_price = sum([b.service.price for b in values])
                new_key = (*k, number_of_bookings, total_price)
                new_keys.append(new_key)
            # Update keys to contain more meta data.
            old_keys = upcoming_bookings.keys()
            for new_key, old_key in zip(new_keys, old_keys):
                upcoming_bookings[new_key] = upcoming_bookings.pop(old_key)
            print("upcoming_bookings = ", upcoming_bookings)
    else:
        # Return details for specified booking
        booking = Booking.query.get(booking_id)
        if booking:
            form.set_data_from_model(booking)
        else:
            flash(f"Booking not found.", "error")
    return render_template(
        "admin/booking.html",
        booking=booking,
        upcoming_bookings=upcoming_bookings,
        previous_bookings=previous_bookings,
        form=form,
    )


@booking_bp.route("/add", methods=["POST"])
@login_required
def add():
    form = BookingForm()
    if form.validate_on_submit():
        data = form.data
        data["user_id"] = current_user.id
        Booking.add(data)
        flash(f"Booking added successfully!", "success")
    return redirect(url_for("booking_bp.get"))


@booking_bp.route("/update/<int:booking_id>", methods=["POST", "PUT"])
@login_required
def update(booking_id: int):
    booking = Booking.query.get(booking_id)
    form = BookingForm()
    if booking and form.validate_on_submit():
        booking.update(form.data)
        flash("Booking updated successfully!", "success")
    else:
        flash("Booking not found.", "error")
    return redirect(url_for("booking_bp.get"))


@booking_bp.route("/delete/<int:booking_id>", methods=["POST", "DELETE"])
@login_required
def delete(booking_id: int):
    booking = Booking.query.get(booking_id)
    if booking:
        booking.delete()
        flash("Booking deleted successfully!", "success")
    else:
        flash("Booking not found.", "error")
    return redirect(url_for("booking_bp.get"))
