import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

# from flask_minify import Minify
from flask_sqlalchemy import SQLAlchemy
from flask_wallet_of_satoshi import WalletOfSatoshi
from flask_wtf.csrf import CSRFProtect
from htmlmin.main import minify
from loguru import logger

# Configure logger
logger.debug("Configuring logger ...")
LOGURU_LEVEL = os.getenv("LOGURU_LEVEL", "INFO")
LOGURU_LEVEL = LOGURU_LEVEL.upper()
logger.remove()
logger.add(sys.stderr, level=LOGURU_LEVEL)
logger.debug(f"{LOGURU_LEVEL = }")

# Register globals

logger.debug("Creating global external instances ...")
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
# minify = Minify()
wos = WalletOfSatoshi()

# Middleware Methods

from urllib.parse import urlparse
from flask import request, Response


def htmx_middleware(response: Response) -> Response:
    hx_request = request.headers.get("HX-Request")
    status_code = response.status_code
    if hx_request == "true" and status_code == 302:
        logger.debug(f"{hx_request = } {status_code = }")
        ref_header = request.headers.get("Referer", "")
        logger.debug(f"{ref_header = }")
        if ref_header:
            referer = urlparse(ref_header)
            logger.debug(f"{referer = }")
            querystring = f"?next={referer.path}"
            logger.debug(f"{querystring = }")
        else:
            querystring = ""
        redirect = urlparse(response.location)
        response.status_code = 204
        response.headers["HX-Redirect"] = f"{redirect.path}{querystring}"
    return response


# Create application


def create_app(Config) -> Flask:
    logger.debug("Creating application ...")

    app = Flask(__name__, instance_relative_config=True)

    logger.debug("Configuring application ...")
    app.config.from_object(Config)

    logger.debug("Creating external global instances ...")
    csrf.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app, db)
    login_manager.init_app(app=app)
    mail.state = mail.init_app(app=app)
    # minify.init_app(app=app)
    wos.init_app(app=app)

    with app.app_context():
        # Configure login manager

        from services import user_service
        from models.user import User

        logger.debug("Configuring login manager ...")
        login_manager.login_view = "auth_bp.sign_in"
        login_manager.login_message_category = "error"
        # login_manager.session_protection = "strong"

        @login_manager.user_loader
        def load_user(user_id: int) -> User:
            user = user_service.get_user_by_id(int(user_id))
            logger.debug(f"Loaded {user = }")
            return user

        # Import and register public pages

        logger.debug("Importing and registering public routes ...")

        from blueprints.index_bp import index_bp
        from blueprints.legal_bp import legal_bp
        from blueprints.sign_up_bp import sign_up_bp

        app.register_blueprint(index_bp, url_prefix="/")
        app.register_blueprint(legal_bp, url_prefix="/legal")
        app.register_blueprint(sign_up_bp, url_prefix="/sign-up")

        # Import and register dashboard pages

        logger.debug("Importing and registering dashboard routes ...")

        from blueprints.dashboard.dashboard_bp import dashboard_bp
        from blueprints.dashboard.auth_bp import auth_bp
        from blueprints.dashboard.booking_bp import booking_bp
        from blueprints.dashboard.customer_bp import customer_bp
        from blueprints.dashboard.dog_bp import dog_bp
        from blueprints.dashboard.vet_bp import vet_bp
        from blueprints.dashboard.expense_bp import expense_bp
        from blueprints.dashboard.service_bp import service_bp
        from blueprints.dashboard.invoice_bp import invoice_bp

        app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
        app.register_blueprint(auth_bp, url_prefix="/dashboard/auth")
        app.register_blueprint(booking_bp, url_prefix="/dashboard/bookings")
        app.register_blueprint(customer_bp, url_prefix="/dashboard/customers")
        app.register_blueprint(dog_bp, url_prefix="/dashboard/dogs")
        app.register_blueprint(vet_bp, url_prefix="/dashboard/vets")
        app.register_blueprint(expense_bp, url_prefix="/dashboard/expenses")
        app.register_blueprint(service_bp, url_prefix="/dashboard/services")
        app.register_blueprint(invoice_bp, url_prefix="/dashboard/invoices")

        from blueprints.dashboard.booking_htmx_bp import booking_htmx_bp

        app.register_blueprint(booking_htmx_bp, url_prefix="/bookings")

        from blueprints.app_bp import app_bp

        app.register_blueprint(app_bp, url_prefix="/app")

        # Middleware

        from datetime import datetime
        from flask import flash, redirect, Response, url_for

        @app.context_processor
        def handle_context():
            return {"now": datetime.utcnow()}

        @app.errorhandler(400)
        def handle_bad_request(e):
            # logger.error(f"Bad request: {e}")
            flash(f"Ut-oh! {e}", "error")
            return redirect(url_for("auth_bp.sign_in"))

        @app.errorhandler(403)
        def handle_expired_token(e):
            # logger.error(f"Expired token: {e}")
            return redirect(url_for("auth_bp.sign_in"))

        @app.errorhandler(404)
        def page_not_found(e):
            # logger.error(f"Page not found: {e}")
            return "This page does not exist", 404

        @app.before_request
        def before_request_func():
            # logger.debug("before_request_func")
            return

        @app.after_request
        def after_request_func(response: Response) -> Response:
            # logger.debug(f"{response = }")
            response = htmx_middleware(response)
            logger.debug(f"{response = }")
            return response

        logger.debug("Returning the application ...")
        return app
