import os

from .base import *  # noqa
from .sentry_conf import *  # noqa

SERVER_IP = os.environ["SERVER_IP"]
SERVER_DOMAIN = os.environ["SERVER_DOMAIN"]

# Required in production — no insecure fallbacks
SECRET_KEY = os.environ["SECRET_KEY"]
DATABASES["default"].update(  # noqa: F405
    HOST=os.environ["POSTGRES_HOST"],
    NAME=os.environ["POSTGRES_DB"],
    PORT=os.environ["POSTGRES_PORT"],
    USER=os.environ["POSTGRES_USER"],
    PASSWORD=os.environ["POSTGRES_PASSWORD"],
)

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = [SERVER_IP, SERVER_DOMAIN]

# Allow ip and domain
ALLOWED_IPS_AND_DOMAINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    f"https://www.{SERVER_DOMAIN}",
    f"http://www.{SERVER_DOMAIN}",
    f"https://{SERVER_DOMAIN}",
    f"http://{SERVER_DOMAIN}",
]
# CSRF
CSRF_TRUSTED_ORIGINS = ALLOWED_IPS_AND_DOMAINS
# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
] + ALLOWED_IPS_AND_DOMAINS

# Swagger settings
SPECTACULAR_SETTINGS["SERVERS"] = [  # noqa: F405
    {"url": f"https://{SERVER_DOMAIN}", "description": "Production server"},
]

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = True
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# STATIC
# ------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
