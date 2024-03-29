from datetime import date, datetime, timedelta, time
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from models.customer import Customer
from models.service import Service
from utils.form_mixin import FormMixin


def get_time_choices(
    start_hour: int = 8, end_hour: int = 18, interval_minutes: int = 15
):
    working_hours_start = time(start_hour, 0)
    working_hours_end = time(end_hour, 0)
    time_interval = timedelta(minutes=interval_minutes)
    time_choices = []
    current_time = datetime.combine(datetime.today(), working_hours_start)
    end_time = datetime.combine(datetime.today(), working_hours_end)
    while current_time <= end_time:
        time_choices.append(
            (current_time.strftime("%H:%M"), current_time.strftime("%I:%M %p"))
        )
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
    time = SelectField("Time", validators=[DataRequired()], choices=time_choices)
    customer_id = SelectField("Customer", coerce=int, validators=[DataRequired()])
    service_id = SelectField("Service", coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer_id.choices = [
            (customer.id, customer.name)
            for customer in Customer.query.order_by(Customer.name).all()
        ]
        self.service_id.choices = [
            (service.id, service.name)
            for service in Service.query.order_by(Service.name).all()
        ]
