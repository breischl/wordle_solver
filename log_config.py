import logging
import logging.config

logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s %(message)s",
            "validate": "True"
        },

    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    }
})
logging.getLogger(__name__).debug("Logging configured")
