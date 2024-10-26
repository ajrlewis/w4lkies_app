from typing import Optional

from loguru import logger

from app import db
from models.user import User


def get(user_id: int) -> User:
    user = db.session.get(User, user_id)
    return user


def get_all() -> list[User]:
    users = db.session.query(User).all()
    return users
