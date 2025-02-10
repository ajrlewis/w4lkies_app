import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import desc

from app import db
from forms.customer_form import CustomerForm
from models.customer import Customer


def get_customer_form(customer: Optional[Customer] = None) -> CustomerForm:
    customer_form = CustomerForm()
    if customer:
        customer_form.set_data_from_model(customer)
    return customer_form


def get_customers() -> list[Customer]:
    customers = db.session.query(Customer).all()
    logger.debug(f"{customers = }")
    return customers


def get_customer_by_id(customer_id: int) -> Optional[Customer]:
    customer = db.session.get(Customer, customer_id)
    logger.debug(f"{customer = }")
    return customer


def add_customer(customer_data: dict) -> Optional[Customer]:
    new_customer = Customer(
        name=dog_data.get("name"),
        phone=dog_data.get("phone"),
        email=dog_data.get("email"),
        emergency_contact_name=dog_data.get("emergency_contact_name"),
        emergency_contact_phone=dog_data.get("emergency_contact_phone"),
        signed_up_on=dog_data.get("signed_up_on", f"{datetime.datetime.now()}"),
        is_active=True,
    )
    try:
        db.session.add(new_customer)
        db.session.commit()
        logger.debug(f"{new_customer = }")
        return new_customer
    except Exception as e:
        logger.error(f"Error adding customer: {e}")
        db.session.rollback()
        return
