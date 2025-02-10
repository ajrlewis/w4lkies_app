from typing import Optional

from loguru import logger
from werkzeug.security import generate_password_hash

from app import db
from forms.user_form import UserForm
from models.user import User


def get_password_hash(password: str) -> str:
    password_hash = generate_password_hash(password, method="scrypt")
    return password_hash


def get_user_form(user: Optional[User] = None) -> UserForm:
    logger.debug(f"{user = }")
    user_form = UserForm(obj=None)
    if user:
        user_form.set_data_from_model(user)
    return user_form


def get_user_by_id(user_id: int) -> Optional[User]:
    user = db.session.get(User, user_id)
    return user


def get_user_by_email(email: str) -> Optional[User]:
    user = db.session.query(User).filter_by(email=email).first()
    return user


def get_users(
    name: Optional[str] = None,
    email: Optional[str] = None,
    is_admin: Optional[bool] = None,
    sort_by: str = "name",
    sort_order: str = "asc",
) -> list[User]:
    query = db.session.query(User)

    # Apply filtering of companies
    if name:
        logger.debug(f"{name = }")
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        logger.debug(f"{email = }")
        query = query.filter(Company.email.ilike(f"%{email}%"))

    # Apply sorting
    if sort_by == "name":
        if sort_order == "asc":
            order_by = User.name.asc()
        else:
            order_by = User.name.desc()
        query = query.order_by(order_by)

    users = query.all()

    # # Get first page of users
    # users = query.paginate(
    #     page=pagination_parameters.page,
    #     per_page=pagination_parameters.page_size,
    #     count=True,
    #     error_out=False,
    # )

    # # Update pagination parameters
    # pagination_parameters.item_count = query.count()

    return users


def update_user_by_id(user_id: int, user_data: dict) -> Optional[User]:
    logger.debug(f"{user_id = } {user_data = }")

    user = get_user_by_id(user_id)
    logger.debug(f"{user = }")
    if not user:
        logger.error(f"{user_id} not found.")
        return

    if name := user_data.get("name"):
        logger.debug(f"{name = }")
        user.name = name

    if email := user_data.get("email"):
        logger.debug(f"{email = }")
        user.email = email

    is_admin = user_data.get("is_admin")
    if is_admin is not None:
        logger.debug(f"{is_admin = }")
        user.is_admin = is_admin

    try:
        db.session.commit()
        return user
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        db.session.rollback()
        return


def add_user(user_data: dict) -> Optional[User]:
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


def delete_user_by_id(user_id: int) -> None:
    user = get_user_by_id(user_id)
    logger.debug(f"{user = }")
    if user is not None:
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete user: {e}")
    else:
        logger.error(f"User with ID {user_id} does not exist")
