import sys

sys.path.append("./")

from datetime import date
import json
import re
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


def read_csv(filename: str, model: db.Model):
    with app.app_context():
        df = pd.read_csv(filename)
        df = df.replace(np.nan, None)
        columns = [c for c in df.columns if c.startswith("is_")]
        df[columns] = df[columns].astype(bool)
        for _, row in df.iterrows():
            obj = model(**row.to_dict())
            db.session.add(obj)
            db.session.commit()


def restore_from_csvs():
    drop_database_tables()
    create_database_tables()
    read_csv("data/customers.csv", Customer)
    read_csv("data/vets.csv", Vet)
    read_csv("data/dog_breeds.csv", DogBreed)
    read_csv("data/dogs.csv", Dog)
    read_csv("data/services.csv", Service)
    read_csv("data/invoices.csv", Invoice)
    read_csv("data/bookings.csv", Booking)


def write_csv(filename: str, model: db.Model):
    with app.app_context():
        result = model.query.all()
        df = pd.DataFrame([vars(obj) for obj in result])
        df.to_csv(filename, index=False)


def print_schema():
    print(f"{CreateTable(Customer.__table__)},")
    print(f"{CreateTable(Vet.__table__)},")
    print(f"{CreateTable(DogBreed.__table__)},")
    print(f"{CreateTable(Dog.__table__)},")
    print(f"{CreateTable(Service.__table__)},")
    print(f"{CreateTable(Invoice.__table__)},")
    print(f"{CreateTable(Booking.__table__)},")
    print(f"{CreateTable(User.__table__)},")


def main():
    pass


if __name__ == "__main__":
    main()
