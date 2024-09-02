import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wallet_of_satoshi import WalletOfSatoshi
from flask_wtf.csrf import CSRFProtect
from htmlmin.main import minify
from loguru import logger

# Configure Loguru

LOGURU_LEVEL = os.getenv("LOGURU_LEVEL", "INFO")
LOGURU_LEVEL = LOGURU_LEVEL.upper()

logger.remove()
logger.add(sys.stderr, level=LOGURU_LEVEL)
logger.debug(f"{LOGURU_LEVEL = }")


# from flask_minify import Minify

# Register globals

logger.debug("Creating global external instances ...")

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
# minify = Minify()
wos = WalletOfSatoshi()

# Configure login manager

logger.debug("Configuring login manager ...")

from models.user import User

login_manager.login_view = "auth_bp.sign_in"
login_manager.login_message_category = "error"
# login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id: int) -> User:
    user = User.query.get(int(user_id))
    logger.info(f"Loaded {user = } ...")
    return user


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
        logger.debug(
            "Creating all tables needed (probably migrations should handle this!) ..."
        )

        # db.create_all()

        # TODO (ajrl) Move this to own module:
        @app.context_processor
        def handle_context():
            from datetime import datetime

            return {"now": datetime.utcnow()}

        # Import home page
        logger.debug("Importing routes ...")

        from blueprints.index_bp import index_bp
        from blueprints.legal_bp import legal_bp
        from blueprints.public.sign_up_bp import sign_up_bp

        app.register_blueprint(index_bp, url_prefix="/")
        app.register_blueprint(legal_bp, url_prefix="/legal")
        app.register_blueprint(sign_up_bp, url_prefix="/sign-up")

        # Import and register dashboard pages

        from blueprints.dashboard.dashboard_bp import dashboard_bp
        from blueprints.dashboard.auth_bp import auth_bp
        from blueprints.dashboard.booking_bp import booking_bp

        app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
        app.register_blueprint(auth_bp, url_prefix="/dashboard/auth")
        app.register_blueprint(booking_bp, url_prefix="/dashboard/bookings")

        #

        from blueprints.admin.admin_bp import admin_bp

        # from blueprints.admin.auth_bp import auth_bp
        from blueprints.admin.customer_bp import customer_bp
        from blueprints.admin.dog_bp import dog_bp
        from blueprints.admin.dog_breed_bp import dog_breed_bp
        from blueprints.admin.vet_bp import vet_bp
        from blueprints.admin.service_bp import service_bp
        from blueprints.admin.invoice_bp import invoice_bp
        from blueprints.admin.expense_bp import expense_bp
        from blueprints.admin.verify_sign_up_bp import verify_sign_up_bp

        logger.debug("Registering routes ...")

        # app.register_blueprint(admin_bp, url_prefix="/dashboard")
        # app.register_blueprint(auth_bp, url_prefix="/dashboard/auth")
        app.register_blueprint(customer_bp, url_prefix="/dashboard/customers")
        app.register_blueprint(dog_bp, url_prefix="/dashboard/dogs")
        app.register_blueprint(dog_breed_bp, url_prefix="/dashboard/dog-breeds")
        app.register_blueprint(vet_bp, url_prefix="/dashboard/vets")
        app.register_blueprint(service_bp, url_prefix="/dashboard/services")
        app.register_blueprint(invoice_bp, url_prefix="/dashboard/invoices")
        app.register_blueprint(expense_bp, url_prefix="/dashboard/expenses")
        app.register_blueprint(
            verify_sign_up_bp, url_prefix="/dashboard/verify-sign-up"
        )

        logger.debug("Returning the application ...")
        return app
