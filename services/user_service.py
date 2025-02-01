from typing import Optional

from loguru import logger
from werkzeug.security import generate_password_hash

from app import db
from models.user import User


def get_user(user_id: int) -> Optional[User]:
    user = db.session.get(User, user_id)
    return user


def get_user_by_email(email: str) -> Optional[User]:
    user = db.session.query(User).filter_by(email=email).first()
    return user


def get_users() -> list[User]:
    users = db.session.query(User).all()
    return users


def add_user(user_data: dict) -> User:
    new_user = User(
        name=user_data.get("name"),
        email=user_data.get("email"),
        password=generate_password_hash(user_data.get("password"), method="scrypt"),
        is_admin=False,
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        logger.debug(f"{new_user = }")
        return new_user
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        db.session.rollback()
        return
