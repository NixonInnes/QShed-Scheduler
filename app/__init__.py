import os
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from qshed.client import QShedClient

from config import config


config = config[os.getenv("APP_CONFIG", "default")]

scheduler = BackgroundScheduler(timezone=config.SCHEDULER_TIMEZONE)
scheduler.add_jobstore("sqlalchemy", url="sqlite:///schedule.db")

client = QShedClient("http://localhost:5000")


def create_app():
    app = FastAPI()

    from .routers import main

    app.include_router(main.router)

    return app
