# import configparser
from datetime import datetime
from io import BytesIO
import sys
import tempfile
from typing import Dict
import pandas as pd
from PIL import Image
import qrcode
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

x_0 = 0.5 * inch
y_0 = 8.25 * inch

font_skip = 0.12 * inch
small_skip = 0.25 * inch
medium_skip = 0.5 * inch
big_skip = 1.0 * inch

# class InvoicePDF:
#     pass


def _add_header(pdf, invoice_data, width, height):
    # Invoice logo
    logo_width = 150
    logo_aspect_ratio = 1.1
    logo_height = logo_aspect_ratio * logo_width
    w, h = pdf.drawInlineImage(
        invoice_data["server_logo_filepath"],
        x_0,
        y_0,
        width=logo_width,
        height=logo_height,
    )
    pdf.linkURL(
        invoice_data["server_url"],
        (x_0, y_0, x_0 + w, y_0 + h),
        thickness=0,
        relative=1,
    )

    # Invoice title
    # pdf.setFont("theme_font_1", 20)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColor(colors.black)
    x = width / 2
    y = 0.9 * height
    text = "Invoice"
    pdf.drawCentredString(x, y, text.upper())

    # Invoice IDs
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.black)
    x = x_0 + 4.25 * inch
    y -= medium_skip
    pdf.drawString(x, y, f"Invoice #: {invoice_data['invoice_number']}")
    y -= small_skip
    pdf.drawString(x, y, f"Invoice Date: {invoice_data['invoice_date']}")
    y -= small_skip
    text = f"Due Date: {invoice_data['invoice_due_date']}"
    pdf.drawString(x, y, text)

    # Email contact for invoice help
    y -= medium_skip
    text = "Need help? "
    pdf.drawString(x, y, text)
    w = pdf.stringWidth(text)
    x += w
    text = invoice_data["server_email"]
    pdf.drawString(x, y, text)
    w = pdf.stringWidth(text)
    h = pdf._leading
    text = f"mailto:{invoice_data['server_email']}?subject=Invoice%20#:%20{invoice_data['invoice_number']}"
    pdf.linkURL(
        text,
        (x, y, x + w, y + h),
        thickness=0,
        relative=1,
    )
    x = x_0 + medium_skip
    y -= big_skip
    return x, y


def _add_page_break(pdf, invoice_data, width, height):
    pdf.showPage()
    x, y = _add_header(pdf, invoice_data, width, height)
    return x, y


def _add_ln_invoice(x, y):
    y = y_payment
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Lightning Invoice:")
    pdf.setFont("Helvetica", 12)
    hh = 12
    qr = qrcode.QRCode(version=1, box_size=2, border=0)
    data = "lightning:" + invoice_data["invoice_payment_request"]
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        img.save(f.name)
        y = y - img.size[1] - small_skip
        w, h = pdf.drawImage(f.name, x, y)
    pdf.setFillColorRGB(1, 1, 1, 0.05)
    img = ImageReader("static/img/bitcoin-lightning.jpeg")
    _ = pdf.drawImage(img, x, y, 0.9 * w, 0.9 * h)
    pdf.linkURL(
        data,
        (x, y, x + w, y + h),
        thickness=0,
        relative=1,
    )
    pdf.setFillColor(colors.black)
    start_chars = invoice_data["invoice_payment_request"][:10]
    end_chars = invoice_data["invoice_payment_request"][-10:]
    display_text = f"{start_chars}...{end_chars}"
    y -= small_skip
    pdf.drawString(x, y, display_text)
    x += 4 * inch
    return x, y


def _create(invoice_data: Dict[str, str]):
    # Create document
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # x = width / 2
    # y = 0.9 * height

    #
    # Header
    #
    x, y = _add_header(pdf, invoice_data, width, height)

    # Invoice to
    pdf.setFont("Helvetica-Bold", 12)
    text = f"Bill To: {invoice_data['customer_name']}"
    pdf.drawString(x, y, text)

    #
    # Table of services.
    #

    table_header = ["Date", "Service", f"Price / {invoice_data['invoice_currency']}"]
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), invoice_data["theme_color_1"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), invoice_data["theme_color_2"]),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ("ALIGN", (0, 1), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 11),
            ("RIGHTPADDING", (2, 1), (2, -1), 5),
            ("RIGHTPADDING", (3, 1), (3, -1), 5),
            ("RIGHTPADDING", (4, 1), (4, -1), 5),
        ]
    )

    invoice_services = invoice_data["invoice_services"]
    service_chunks = chunk_services(invoice_services)
    number_of_chunks = len(service_chunks)

    for i, services in enumerate(service_chunks):
        table_data = [table_header]
        for service in services:
            table_data.append(
                [service["date"], service["service"], f"{service['price']:.2f}"]
            )
        table = Table(table_data, colWidths=[2.16 * inch, 2.16 * inch, 2.16 * inch])
        table.setStyle(table_style)
        w, h = table.wrapOn(pdf, 400, 400)

        x = (width - w) / 2
        if i == 0:
            y -= medium_skip
        else:
            y += font_skip
        y -= h
        table.drawOn(pdf, x, y)

        # Add the subtotal and total on the last chunk of services.
        if i == number_of_chunks - 1:
            # x = (width - w) / 2
            # y -= medium_skip
            # y -= h
            # table.drawOn(pdf, x, y)
            pdf.setFillColor(colors.black)
            x -= 0.75 * inch
            x += 4.8 * inch
            dx = 1.5 * inch
            y -= small_skip
            y -= 0.175 * inch
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.setLineWidth(7)
            pdf.line(x, y, x + dx, y)
            pdf.setStrokeColor(invoice_data["theme_color_3"])
            pdf.setLineWidth(6)
            pdf.line(x, y, x + dx, y)
            discount = invoice_data["invoice_services_price_total_discount"]
            if discount > 0.0:
                y -= small_skip
                y -= 0.175 * inch
                text = f"Discount: {invoice_data['invoice_currency']}{discount:.2f}"
                pdf.drawString(x, y, text)

            y -= small_skip
            text = f"Total: {invoice_data['invoice_currency']}{invoice_data['invoice_services_price_total']:.2f}"
            pdf.drawString(x, y, text)
        # Page break
        x, y = _add_page_break(pdf, invoice_data, width, height)

    #
    # Payment Details
    #
    x_payment = x
    y_payment = y
    # Bank payment details
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Bank Details:")
    pdf.setFont("Helvetica", 12)
    y -= small_skip
    y -= 0.125 * inch
    pdf.drawString(x, y, invoice_data["server_bank_name"])
    y -= small_skip
    pdf.drawString(x, y, "Sort Code: " + invoice_data["server_bank_sort_code"])
    y -= small_skip
    text = "Account Number: " + str(invoice_data["server_bank_account_number"])
    pdf.drawString(x, y, text)

    x = x_payment + 3 * inch
    y = y_payment
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Other Payment Methods:")

    y -= small_skip
    y -= 0.125 * inch
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Want to pay by PayPal? (debit/credit)")
    pdf.setFont("Helvetica", 12)
    y -= small_skip
    pdf.drawString(x, y, "Request a PayPal invoice.")
    y -= small_skip
    pdf.drawString(x, y, "Note a 7% fee will be added to the total.")

    y -= medium_skip
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Want to pay by Bitcoin?")
    pdf.setFont("Helvetica", 12)
    y -= small_skip
    pdf.drawString(x, y, "Request a Bitcoin Lightning invoice.")
    y -= small_skip
    pdf.drawString(x, y, "Or send Bitcoin to pay@w4lkies.com")

    y -= medium_skip
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Want to pay by Cash?")
    pdf.setFont("Helvetica", 12)
    pdf.setFont("Helvetica", 12)
    y -= small_skip
    pdf.drawString(x, y, "Pay in Person")

    #  Footer
    x = width / 2.0

    # TODO (ajrl) small_skip and big_skip, y += small_skip
    y -= big_skip
    y -= big_skip

    text = "Thank you for your business!".upper()
    pdf.setFillColor(colors.black)
    # pdf.setFont("theme_font_1", 12)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(x, y, text)

    # Save invoice
    pdf.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def chunk_services(services: list[str]) -> list[list[str]]:
    maximum_number_of_services_on_first_page = 21
    maximum_number_of_services_for_aggregate = 0
    maximum_number_of_services_on_page = (
        maximum_number_of_services_on_first_page
        + maximum_number_of_services_for_aggregate
    )
    service_chunks = []
    page_number = 0
    while len(services) > 0:
        page_number += 1
        number_of_services_remaining = len(services)
        if page_number == 1:
            number_of_services_on_page = maximum_number_of_services_on_first_page
        else:
            if number_of_services_remaining > maximum_number_of_services_on_page:
                number_of_services_on_page = maximum_number_of_services_on_page
            else:
                number_of_services_on_page = number_of_services_remaining

        service_chunks.append(services[:number_of_services_on_page])
        services = services[number_of_services_on_page:]
    return service_chunks


def create(transactions_df: pd.DataFrame):
    server_name = "w4lkies"
    server_url = "https://w4lkies.com"
    server_logo = "static/img/logo-white-background.png"
    server_email = "hello@w4lkies.com"
    server_bank_name = "Sophia Lewis"
    server_bank_sort_code = "04-29-09"
    server_bank_account_number = "65204158"
    invoice_due_days = 7
    invoice_currency = "£"
    invoice_payment_request = ""
    theme_color_1 = "#fd8927"
    theme_color_2 = "#f4e2cc"
    theme_color_3 = "#8bb4a6"
    theme_font_1 = ""

    invoice_services = [
        {"date": d, "service": s, "price": p}
        for d, s, p in transactions_df[
            ["date", "service_name", "service_price"]
        ].to_numpy()
    ]
    invoice_services_price_subtotal = transactions_df["subtotal_price"][0]
    invoice_services_price_total_discount = transactions_df["total_price_discount"][0]
    invoice_services_price_total = transactions_df["total_price"][0]

    customer_name = transactions_df["customer_name"][0]
    invoice_number = transactions_df["number"][0]
    invoice_date_issued = transactions_df["date_issued"][0]

    invoice_due_date = pd.Timestamp(invoice_date_issued) + pd.Timedelta(
        days=invoice_due_days
    )
    invoice_due_date = f"{invoice_due_date.date()}"

    # pdfmetrics.registerFont(TTFont("theme_font_1", theme_font_1))

    invoice_data = {
        "server_name": server_name,
        "server_url": server_url,
        "server_email": server_email,
        "server_logo_filepath": server_logo,
        "server_bank_name": server_bank_name,
        "server_bank_sort_code": server_bank_sort_code,
        "server_bank_account_number": server_bank_account_number,
        "customer_name": customer_name,
        "invoice_number": invoice_number,
        "invoice_date": f"{invoice_date_issued}",
        "invoice_due_date": f"{invoice_due_date}",
        "invoice_currency": invoice_currency,
        "invoice_payment_request": invoice_payment_request,
        "invoice_services": invoice_services,
        "invoice_services_price_subtotal": invoice_services_price_subtotal,
        "invoice_services_price_total_discount": invoice_services_price_total_discount,
        "invoice_services_price_total": invoice_services_price_total,
        "theme_color_1": theme_color_1,
        "theme_color_2": theme_color_2,
        "theme_color_3": theme_color_3,
        "theme_font_1": theme_font_1,
    }

    pdf = _create(invoice_data)

    return pdf
