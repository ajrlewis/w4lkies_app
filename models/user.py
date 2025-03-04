import datetime
from typing import Optional

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from app import db
from utils.model_mixin import ModelMixin


class User(UserMixin, db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    # otp_secret = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    # role =
    # bio =
    # profile_image =
