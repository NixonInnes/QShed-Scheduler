import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from config import config


config = config[os.getenv("APP_CONFIG", "default")]

scheduler = BackgroundScheduler(timezone=config.SCHEDULER_TIMEZONE)
scheduler.add_jobstore("sqlalchemy", url="sqlite:///schedule.db")


def create_app():
    app = Flask(__name__)

    config.init_app(app)

    from .blueprints.main import main_bp as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
