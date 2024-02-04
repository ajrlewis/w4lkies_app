from typing import List, Optional
from flask_mail import Message
import html2text
from app import mail


def send(
    sender: str,
    recipient: str,
    subject: str,
    html: str,
    attachments: Optional[List] = None,
):
    try:
        recipients = [recipient]
        bcc = [mail.username]
        body = html2text.html2text(html)
        message = Message(
            subject,
            sender=sender,
            bcc=bcc,
            recipients=recipients,
            html=html,
            body=body,
        )
        if attachments:
            for attachment in attachments:
                message.attach(**attachment)
        mail.send(message)
    except Exception as e:
        import traceback as tb

        print(tb.format_exc())
        print(f"Error: {e}")
