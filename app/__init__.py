from flask import Flask
from .middleware.request_logger import RequestLoggerMiddleware
from .models.db import init_db


def create_app(config_name="default"):
    app = Flask(__name__)

    # Load config
    from config.settings import config
    app.config.from_object(config[config_name])

    # Init DB
    init_db(app)

    # Register middleware
    RequestLoggerMiddleware(app)

    # Register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app