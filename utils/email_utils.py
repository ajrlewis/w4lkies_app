import traceback as tb
from typing import Optional

from flask_mail import Message
import html2text
from loguru import logger

from app import mail


def send(
    sender: str,
    recipient: str,
    subject: str,
    html: str,
    attachments: Optional[list] = None,
):
    try:
        recipients = [recipient]
        logger.debug(f"{recipients = }")
        bcc = [mail.username]
        logger.debug(f"{bcc = }")
        body = html2text.html2text(html)
        logger.debug(f"{body = }")
        message = Message(
            subject,
            sender=sender,
            bcc=bcc,
            recipients=recipients,
            html=html,
            body=body,
        )
        logger.debug(f"{message = }")
        if attachments:
            for attachment in attachments:
                logger.debug(f"{attachment = }")
                message.attach(**attachment)
        mail.send(message)
    except Exception as e:
        logger.error(f"{tb.format_exc() = }")
        logger.error(f"{e = }")
