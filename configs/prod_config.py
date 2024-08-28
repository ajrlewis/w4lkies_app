import ast
import datetime
import json
import os
import secrets

from dotenv import load_dotenv

load_dotenv()


class ProdConfig:
    JSON_SORT_KEYS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER_NAME = os.getenv("MAIL_DEFAULT_SENDER_NAME")
    MAIL_USE_TLS = ast.literal_eval(os.getenv("MAIL_USE_TLS"))
    MAIL_USE_SSL = ast.literal_eval(os.getenv("MAIL_USE_SSL"))

    REMEMBER_COOKIE_DURATION = datetime.timedelta(
        seconds=int(os.getenv("REMEMBER_COOKIE_DURATION", 60))
    )
    PERMANENT_SESSION_LIFETIME = REMEMBER_COOKIE_DURATION

    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")

    SECRET_KEY = secrets.token_urlsafe(32)

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = ast.literal_eval(
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    )

    WEBSITE_NAME = os.getenv("WEBSITE_NAME")
    WEBSITE_LTD_NAME = os.getenv("WEBSITE_LTD_NAME")
    WEBSITE_SLOGAN = os.getenv("WEBSITE_SLOGAN")
    WEBSITE_TELEPHONE = os.getenv("WEBSITE_TELEPHONE")
    WEBISTE_ADDRESS = os.getenv("WEBISTE_ADDRESS")
    WEBSITE_URL = os.getenv("WEBSITE_URL")
    WEBSITE_INSTAGRAM = os.getenv("WEBSITE_INSTAGRAM")

    WOS_USERNAME = os.getenv("WOS_USERNAME")
    WOS_USERNAME_ALIAS = os.getenv("WOS_USERNAME_ALIAS")
