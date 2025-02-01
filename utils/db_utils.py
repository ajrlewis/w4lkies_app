from datetime import date
import json
import re
import sys

sys.path.append("./")

import numpy as np
import pandas as pd
from sqlalchemy.schema import CreateTable
from werkzeug.security import generate_password_hash

from app import create_app, db
from models.booking import Booking
from models.customer import Customer
from models.dog import Dog
from models.dog_breed import DogBreed
from models.expense import Expense
from models.expense_type import ExpenseType
from models.invoice import Invoice
from models.service import Service
from models.vet import Vet
from models.user import User

app = create_app()


def phone_format(phone_number):
    # Remove any non-digit characters from the phone number
    digits_only = re.sub(r"\D", "", phone_number)
    digits_only = "%d" % int(digits_only)
    # Check if the phone number is empty or has an invalid length
    if not digits_only or len(digits_only) != 10:
        return phone_number  # Return the original phone number if it's invalid
    formatted_phone_number = f"(+44) {digits_only[:4]} {digits_only[4:]}"
    return formatted_phone_number


def drop_database_tables():
    with app.app_context():
        db.drop_all()
        db.session.commit()


def create_database_tables():
    with app.app_context():
        db.create_all()
        db.session.commit()


def main():
    pass


if __name__ == "__main__":
    main()
