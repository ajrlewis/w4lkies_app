import sys
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_minify import Minify
from flask_sqlalchemy import SQLAlchemy
from flask_wallet_of_satoshi import WalletOfSatoshi
from flask_wtf.csrf import CSRFProtect
from htmlmin.main import minify

csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
minify = Minify()
wos = WalletOfSatoshi()

login_manager = LoginManager()
login_manager.login_view = "auth_bp.sign_in"
login_manager.login_message_category = "error"
# login_manager.session_protection = "strong"


def create_app(Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    csrf.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app, db)
    login_manager.init_app(app=app)
    mail.state = mail.init_app(app=app)
    minify.init_app(app=app)
    wos.init_app(app=app)
    with app.app_context():
        db.create_all()

        # TODO (ajrl) Move this to own module:
        @app.context_processor
        def handle_context():
            from datetime import datetime

            return {"now": datetime.utcnow()}

        # Import and register public pages
        from blueprints.index_bp import index_bp

        # from blueprints.index_bp import index_bp

        # from blueprints.public.index_bp import index_bp
        # from blueprints.public.about_bp import about_bp
        # from blueprints.public.download_bp import download_bp
        # from blueprints.public.gallery_bp import gallery_bp
        # from blueprints.public.contact_bp import contact_bp

        # # from blueprints.public.pay_bp import pay_bp
        from blueprints.public.legal_bp import legal_bp
        from blueprints.public.sign_up_bp import sign_up_bp

        app.register_blueprint(index_bp, url_prefix="/")
        # app.register_blueprint(about_bp, url_prefix="/about")
        # app.register_blueprint(download_bp, url_prefix="/download")
        # app.register_blueprint(gallery_bp, url_prefix="/gallery")
        # app.register_blueprint(contact_bp, url_prefix="/contact")
        # # app.register_blueprint(pay_bp, url_prefix="/pay")
        app.register_blueprint(legal_bp, url_prefix="/legal")
        app.register_blueprint(sign_up_bp, url_prefix="/sign-up")

        # Import and register admin pages
        from blueprints.admin.admin_bp import admin_bp
        from blueprints.admin.auth_bp import auth_bp
        from blueprints.admin.customer_bp import customer_bp
        from blueprints.admin.dog_bp import dog_bp
        from blueprints.admin.dog_breed_bp import dog_breed_bp
        from blueprints.admin.vet_bp import vet_bp
        from blueprints.admin.service_bp import service_bp
        from blueprints.admin.booking_bp import booking_bp
        from blueprints.admin.invoice_bp import invoice_bp
        from blueprints.admin.expense_bp import expense_bp
        from blueprints.admin.user_bp import user_bp
        from blueprints.admin.verify_sign_up_bp import verify_sign_up_bp

        app.register_blueprint(admin_bp, url_prefix="/admin")
        app.register_blueprint(auth_bp, url_prefix="/admin/auth")
        app.register_blueprint(customer_bp, url_prefix="/admin/customers")
        app.register_blueprint(dog_bp, url_prefix="/admin/dogs")
        app.register_blueprint(dog_breed_bp, url_prefix="/admin/dog-breeds")
        app.register_blueprint(vet_bp, url_prefix="/admin/vets")
        app.register_blueprint(service_bp, url_prefix="/admin/services")
        app.register_blueprint(booking_bp, url_prefix="/admin/bookings")
        app.register_blueprint(invoice_bp, url_prefix="/admin/invoices")
        app.register_blueprint(expense_bp, url_prefix="/admin/expenses")
        app.register_blueprint(user_bp, url_prefix="/admin/users")
        app.register_blueprint(verify_sign_up_bp, url_prefix="/admin/verify-sign-up")

        return app
