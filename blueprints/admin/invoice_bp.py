from datetime import date
import hashlib
from io import BytesIO
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import login_required
import pandas as pd
from sqlalchemy import desc
from app import db
from forms.invoice_form import InvoiceForm
from models.booking import Booking
from models.customer import Customer
from models.invoice import Invoice
from utils import invoice_utils

invoice_bp = Blueprint("invoice_bp", __name__)


@invoice_bp.route("/", methods=["GET"])
@invoice_bp.route("/<int:invoice_id>", methods=["GET"])
@login_required
def get(invoice_id: int = None):
    invoices = None
    invoice = None
    invoice_form = InvoiceForm()
    invoice_analytics = {}
    if invoice_id is None:
        invoices = Invoice.query.order_by(desc(Invoice.date_issued)).all()
    else:
        invoice = Invoice.query.get(invoice_id)
        if invoice:
            invoice_form.set_data_from_model(invoice)
        else:
            flash(f"Invoice not found.", "error")
    return render_template(
        "admin/invoice.html",
        invoice=invoice,
        invoices=invoices,
        invoice_form=invoice_form,
        invoice_analytics=invoice_analytics,
    )


@invoice_bp.route("/add", methods=["POST"])
@login_required
def add():
    form = InvoiceForm()
    if form.validate_on_submit():
        customer_id = form.customer_id.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        bookings = Booking.query.filter(
            Booking.date >= start_date,
            Booking.date <= end_date,
            Booking.customer_id == customer_id,
        ).all()
        bookings_df = pd.DataFrame(
            [(t.date, t.service_id) for t in bookings],
            columns=["date", "service_id"],
        )

        # Add discounts
        discount_mask = bookings_df["service_id"].isin([2, 4])
        bookings_df = bookings_df[discount_mask]
        discount = 10.0
        if bookings_df["service_id"].isin([4]).any():
            discount = 7.5
        bookings_df["week"] = bookings_df["date"].apply(lambda d: pd.Timestamp(d).week)
        discount_df = bookings_df.groupby("week").size().reset_index(name="count")
        discount_df["count"] = discount_df["count"] // 3
        discount_df = discount_df[discount_df["count"] >= 1]

        subtotal_price = sum([t.service.price for t in bookings])
        total_price_discount = len(discount_df) * discount
        total_price = subtotal_price - total_price_discount

        invoice_number = (
            hashlib.sha256(f"{customer_id}-{start_date}-{end_date}".encode("UTF-8"))
            .hexdigest()[:6]
            .upper()
        )

        new_invoice = Invoice(
            invoice_number=invoice_number,
            start_date=start_date,
            end_date=end_date,
            date_issued=date.today(),
            subtotal_price=subtotal_price,
            total_price_discount=total_price_discount,
            total_price=total_price,
        )
        new_invoice.bookings = bookings
        db.session.add(new_invoice)
        db.session.commit()

        flash(f"Invoice added successfully!", "success")
    else:
        flash(f"Invoice not added.", "error")
    return redirect(url_for("invoice_bp.get"))


@invoice_bp.route("/update/<int:invoice_id>", methods=["POST", "PUT"])
@login_required
def update(invoice_id: int):
    invoice_id = Invoice.query.get(invoice_id)
    form = InvoiceForm()
    if invoice and form.validate_on_submit():
        invoice.update(form.data)
        flash("Invoice updated successfully!", "success")
    else:
        flash("Invoice not found.", "error")
    return redirect(url_for("invoice_bp.get"))


@invoice_bp.route("/delete/<int:invoice_id>", methods=["POST", "DELETE"])
@login_required
def delete(invoice_id: int):
    invoice = Invoice.query.get(invoice_id)
    if invoice:
        invoice.delete()
        flash("Invoice deleted successfully!", "success")
    else:
        flash("Invoice not found.", "error")
    return redirect(url_for("invoice_bp.get"))


@invoice_bp.route("/download/<int:invoice_id>")
@login_required
def download(invoice_id: int):
    invoice = db.session.get(Invoice, invoice_id)
    db.session.refresh(invoice)
    invoice_data = []
    for booking in invoice.bookings:
        date = booking.date
        month = date.strftime("%B")
        customer_name = booking.customer.name
        dog_name = booking.customer.dogs[0].name
        service_name = booking.service.name
        service_price = booking.service.price
        invoice_data.append(
            {
                "date": f"{date}",
                "customer_name": customer_name,
                "service_name": service_name,
                "service_price": service_price,
            }
        )
    invoice_df = pd.DataFrame(invoice_data)
    invoice_df["number"] = invoice.invoice_number
    invoice_df["date_issued"] = invoice.date_issued
    invoice_df["subtotal_price"] = invoice.subtotal_price
    invoice_df["total_price_discount"] = invoice.total_price_discount
    invoice_df["total_price"] = invoice.total_price
    invoice_pdf = invoice_utils.create(invoice_df)
    download_name = f"{dog_name} {month}.pdf"
    pdf_file = BytesIO()
    pdf_file.write(invoice_pdf)
    pdf_file.seek(0)
    return send_file(
        pdf_file,
        as_attachment=True,
        download_name=download_name,
        mimetype="application/pdf",
    )


@invoice_bp.route("/summary", methods=["GET"])
@login_required
def summary():
    invoices = Invoice.query.all()
    df = pd.DataFrame(
        [
            {
                "date": pd.Timestamp(i.start_date + (i.end_date - i.start_date) / 2),
                "price": i.total_price,
            }
            for i in invoices
        ]
    )
    df["year"] = df["date"].apply(lambda d: d.year)
    df["month"] = df["date"].apply(lambda d: d.month)
    df = df[["year", "month", "price"]].groupby(["year", "month"]).sum().reset_index()
    df["price_cumsum"] = df["price"].cumsum()
    data = df.to_dict(orient="records")
    return {"data": data}, 200
