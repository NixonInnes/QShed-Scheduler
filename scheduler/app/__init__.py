import os
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from qshed.client import QShedClient

from config import config


config = config[os.getenv("APP_CONFIG", "default")]
client = QShedClient(config.GATEWAY_ADDRESS)


def create_app():
    app = FastAPI()

    from .routers import main

    app.include_router(main.router)

    return app


def create_scheduler():
    scheduler = BackgroundScheduler(timezone=config.SCHEDULER_TIMEZONE)
    scheduler.add_jobstore("sqlalchemy", url="sqlite:///schedule.db")
    return scheduler
