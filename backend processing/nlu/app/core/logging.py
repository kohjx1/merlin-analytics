from typing import Type
from pydantic import BaseModel
from logging.config import dictConfig


class LogMessages:
    @staticmethod
    def UNSUPPORTED_MODEL(model_name):
        return "{} is currently not supported".format(model_name)
    
    @staticmethod
    def REQUEST_EXCEPTION(e):
        return "Request exception : {}".format(e)
    
    @staticmethod
    def FATAL_EXCEPTION(e):
        return "Fatal exception : {}".format(repr(e))

    @staticmethod
    def DAO_ERROR(e):
        return "Key not found in document: {}".format(repr(e))


class LogConfig(BaseModel):
    """
    Logging configuration to be set for the server
    """
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(name)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "engine_manager": {"handlers": ["default"], "level": LOG_LEVEL},
        "form_manager": {"handlers": ["default"], "level": LOG_LEVEL},
        "DAO": {"handlers": ["default"], "level": LOG_LEVEL},
    }


def configure_logging() -> None:
    dictConfig(LogConfig().dict())
