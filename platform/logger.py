import logging
import logging.config


ERROR_LOG_FILENAME = 'queues.log'

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "logfile": {  # The handler name
            "formatter": "default",  # Refer to the formatter defined above
            "level": "ERROR",  # FILTER: Only ERROR and CRITICAL logs
            "class": "logging.handlers.RotatingFileHandler",  # OUTPUT: Which class to use
            "filename": ERROR_LOG_FILENAME,  # Param for class above. Defines filename to use, load it from constant
            "backupCount": 2,  # Param for class above. Defines how many log files to keep as it grows
        },
        "console": {  # The handler name
            "formatter": "default",  # Refer to the formatter defined above
            "level": "DEBUG",  # FILTER: All logs
            "class": "logging.StreamHandler",  # OUTPUT: Which class to use
        },
    },
    "loggers": {
        "queues": {  # The name of the logger, this SHOULD match your module!
            "level": "INFO",  # FILTER: only INFO logs onwards from "tryceratops" logger
            "handlers": [
                "logfile",
                "console",  # Refer the handler defined above
            ],
        },
    },
}


def setup_logger():
    logging.config.dictConfig(LOGGING_CONFIG)
