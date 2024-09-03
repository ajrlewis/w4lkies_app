from functools import wraps

from flask import render_template
from flask_login import current_user
from loguru import logger


def admin_user_required(f):
    @wraps(f)
    def _admin_user_required(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            code = 403
            message = "The current user does not have permissions to view this page."
            logger.error(message)
            return render_template("error.html", code=code, message=message)

    return _admin_user_required
