from datetime import date, datetime, timedelta, time

from flask_wtf import FlaskForm
from loguru import logger
from wtforms import SelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired

from models.customer import Customer
from models.service import Service
from models.user import User
from utils.form_mixin import FormMixin


def get_time_choices(start_hour: int, end_hour: int, interval_minutes: int):
    working_hours_start = time(start_hour, 0)
    working_hours_end = time(end_hour, 0)
    time_interval = timedelta(minutes=interval_minutes)
    time_choices = []
    current_time = datetime.combine(datetime.today(), working_hours_start)
    end_time = datetime.combine(datetime.today(), working_hours_end)
    while current_time <= end_time:
        time_choice = (
            current_time.strftime("%H:%M:%S"),
            current_time.strftime("%I:%M %p"),
        )
        time_choices.append(time_choice)
        current_time += time_interval
    return time_choices


time_choices = get_time_choices(start_hour=8, end_hour=18, interval_minutes=15)


class BookingForm(FlaskForm, FormMixin):
    date = DateField(
        "Date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
        render_kw={"placeholder": "yyyy-mm-dd"},
    )
    time = SelectField("Time", validators=[DataRequired()])
    user_id = SelectField("User", coerce=int, validators=[DataRequired()])
    customer_id = SelectField("Customer", coerce=int, validators=[DataRequired()])
    service_id = SelectField("Service", coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time.choices = time_choices
        self.user_id.choices = [
            (user.id, user.name) for user in User.query.order_by(User.name).all()
        ]
        customers = (
            Customer.query.filter_by(is_active=True).order_by(Customer.name).all()
        )
        self.customer_id.choices = [(c.id, c.name) for c in customers]
        services = Service.query.filter_by(is_active=True).order_by(Service.name).all()
        self.service_id.choices = [(s.id, s.name) for s in services]
