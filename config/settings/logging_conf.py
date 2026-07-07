from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Rotating log files: 5MB x 5 files each, in <project>/logs/ (bind-mounted in
# Docker, so production logs are readable from the project root on the host):
#   logs/access.log — request/server activity (INFO+)
#   logs/errors.log — application errors (ERROR+)
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_MAX_BYTES = 5 * 1024 * 1024  # 5MB
LOG_BACKUP_COUNT = 5

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "handlers": {
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
        "": {"level": "ERROR", "handlers": ["errors_file"]},
        # request activity: INFO+ to access.log, errors also to errors.log
        "django.request": {
            "level": "INFO",
            "handlers": ["access_file", "errors_file"],
            "propagate": False,
        },
        # runserver request lines (dev)
        "django.server": {
            "level": "INFO",
            "handlers": ["access_file"],
            "propagate": False,
        },
    },
}
