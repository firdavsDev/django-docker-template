import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Rotating log files: 5MB x 5 files each, in <project>/logs/ (bind-mounted in
# Docker, so production logs are readable from the project root on the host):
#   logs/access.log — request/server activity (INFO+)
#   logs/errors.log — application errors (ERROR+)
# Everything also goes to stdout so `docker logs` / compose json-file rotation
# capture it.
LOG_DIR = BASE_DIR / "logs"
try:
    LOG_DIR.mkdir(exist_ok=True)
except OSError:
    pass

LOG_MAX_BYTES = 5 * 1024 * 1024  # 5MB
LOG_BACKUP_COUNT = 5
APP_LOG_LEVEL = os.environ.get("APP_LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "access_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": str(LOG_DIR / "access.log"),
            "maxBytes": LOG_MAX_BYTES,
            "backupCount": LOG_BACKUP_COUNT,
            "delay": True,
        },
        "errors_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": str(LOG_DIR / "errors.log"),
            "maxBytes": LOG_MAX_BYTES,
            "backupCount": LOG_BACKUP_COUNT,
            "delay": True,
        },
    },
    "loggers": {
        # application errors
        "": {"level": "ERROR", "handlers": ["console", "errors_file"]},
        # project code (src.apps.*): INFO+ to stdout + access.log, errors also
        # to errors.log
        "src": {
            "level": APP_LOG_LEVEL,
            "handlers": ["console", "access_file", "errors_file"],
            "propagate": False,
        },
        # request activity: INFO+ to access.log, errors also to errors.log
        "django.request": {
            "level": "INFO",
            "handlers": ["console", "access_file", "errors_file"],
            "propagate": False,
        },
        # runserver request lines (dev)
        "django.server": {
            "level": "INFO",
            "handlers": ["console", "access_file"],
            "propagate": False,
        },
    },
}
