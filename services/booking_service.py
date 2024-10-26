import datetime
from typing import Optional

from loguru import logger
import pandas as pd
from sqlalchemy import desc

from app import db
from forms.booking_form import BookingForm
from forms.dashboard.booking_filter_form import BookingFilterForm
from models.booking import Booking

booking_date_format = "%Y-%m-%d"
booking_time_format = "%H:%M:%S"
booking_datetime_format = f"{booking_date_format} {booking_time_format}"


def get_form(booking: Optional[Booking] = None) -> BookingForm:
    booking_form = BookingForm()
    if booking:
        booking_form.set_data_from_model(booking)
        booking_form.time.data = booking.time.strftime(booking_time_format)
    return booking_form


def get_filter_form() -> BookingFilterForm:
    booking_filter_form = BookingFilterForm()
    return booking_filter_form


def get(booking_id: int) -> Booking:
    booking = db.session.get(Booking, booking_id)
    return booking


def get_all(
    user_id: Optional[int] = None,
    date_min: Optional[str] = None,
    date_max: Optional[str] = None,
    order_by: Optional[tuple] = (Booking.date.desc(), Booking.time.asc()),
) -> list[Booking]:
    query = db.session.query(Booking)
    if user_id and user_id > -1:
        query = query.filter(Booking.user_id == user_id)
    if date_min:
        query = query.filter(Booking.date >= date_min)
    if date_max:
        query = query.filter(Booking.date < date_max)
    if order_by:
        query = query.order_by(*order_by)
    bookings = query.all()
    return bookings


def get_booking_datetime(booking: Booking) -> datetime:
    datetime_string = " ".join(
        [
            booking.date.strftime(booking_date_format),
            booking.time.strftime(booking_time_format),
        ]
    )
    booking_datetime = datetime.datetime.strptime(
        datetime_string, booking_datetime_format
    )
    return booking_datetime


def get_repeating_booking_datetimes(booking: Booking, repeating_weeks: int) -> list:
    booking_datetime = get_booking_datetime(booking)
    next_booking_datetimes = []
    for i in range(repeating_weeks):
        delta_datetime = datetime.timedelta(days=(i + 1) * 7)
        next_booking_datetime = booking_datetime + delta_datetime
        next_booking_datetimes.append(next_booking_datetime)
    return next_booking_datetimes


def add(data: dict) -> list[Booking]:
    booking = Booking.add(data)
    bookings = [booking]
    logger.debug(f"{data = }")
    repeating_weeks = data.get("repeating_weeks")
    logger.debug(f"{repeating_weeks = }")
    if repeating_weeks > 0:
        datetimes = get_repeating_booking_datetimes(booking, repeating_weeks)
        logger.debug(f"{datetimes = }")
        for datetime in datetimes:
            logger.debug(f"{datetime = }")
            repeat_data = data.copy()
            repeat_data["date"] = datetime.date()
            repeat_data["time"] = datetime.time()
            repeat_booking = Booking.add(repeat_data)
            bookings.append(repeat_booking)
    logger.debug(f"{bookings = }")
    return bookings


def update(booking_id: int, data: dict) -> Booking:
    booking = db.session.get(Booking, booking_id)
    if booking:
        booking.update(data)
    return booking


def delete(booking_id: int):
    booking = get(booking_id)
    if booking:
        booking.delete()


def summary(user_id: int):
    logger.debug(f"{user_id = }")
    bookings = db.session.query(Booking).filter_by(user_id=user_id)
    summary_data = [
        {
            "user_name": b.user.name,
            "booking_year": b.date.year,
            "booking_month_number": b.date.month,
            "booking_month": b.date.strftime("%b"),
            "booking_price": b.service.price,
            "booking_duration": b.service.duration,
        }
        for b in bookings
    ]
    logger.debug(f"{summary_data = }")

    summary_df = pd.DataFrame(summary_data)
    summary_gb = summary_df.groupby(
        ["user_name", "booking_year", "booking_month_number"]
    )
    summary_df = summary_gb.agg(
        booking_month=("booking_month", "min"),
        number_of_bookings=("booking_price", len),
        total_price_of_bookings=("booking_price", "sum"),
        total_duration_of_bookings=("booking_duration", "sum"),
    ).reset_index()
    summary_df = summary_df.drop(columns="booking_month_number")

    summary_df["total_duration_of_bookings"] // 60
    summary_df["total_duration_of_bookings_hours"] = (
        summary_df["total_duration_of_bookings"] // 60
    )
    (
        summary_df["total_duration_of_bookings"] / 60
        - summary_df["total_duration_of_bookings_hours"]
    ) * 60
    summary_df["total_duration_of_bookings_minutes"] = (
        summary_df["total_duration_of_bookings"] / 60
        - summary_df["total_duration_of_bookings_hours"]
    ) * 60
    summary_df["total_duration_of_bookings"] = (
        summary_df["total_duration_of_bookings_hours"].astype(str)
        + " hrs "
        + summary_df["total_duration_of_bookings_minutes"].astype(str)
        + " mins"
    )

    logger.debug(summary_df)
