import os
import logging
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))


def gen_uuid():
    import uuid
    return str(uuid.uuid4())


class Config(object):
    LOG_DIR = os.path.join(basedir, "logs")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

    GATEWAY_ADDRESS = os.getenv("GATEWAY_ADDRESS", "http://localhost:4000")

    SCHEDULER_TIMEZONE = "Europe/London"

    REQUEST_DATABASE = "requestHistory"



class DevConfig(Config):
    DEBUG = True
    LOG_DIR = os.path.join(Config.LOG_DIR, "dev")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


class TestConfig(Config):
    TESTING = True
    LOG_DIR = os.path.join(Config.LOG_DIR, "test")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "WARN")


class ProdConfig(Config):
    LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR")


config = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": DevConfig,
}
