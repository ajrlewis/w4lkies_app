# https://github.com/ajrlewis/neurokit

import pandas as pd
from models.booking import Booking


def get_training_data():
    bookings = Booking.query.all()
    data = [
        {"date": b.date.strftime("%Y-%m-%d"), "price": b.service.price}
        for b in bookings
    ]
    bookings = pd.DataFrame(data)
    # Convert the 'date' column to datetime type
    bookings["date"] = pd.to_datetime(bookings["date"])
    # Group by 'date' and calculate the total price and quantity of bookings
    grouped_bookings = bookings.groupby("date").agg({"price": "sum", "date": "count"})
    grouped_bookings.columns = ["total_price", "quantity"]
    print(grouped_bookings)
