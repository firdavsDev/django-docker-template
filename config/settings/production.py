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

ALLOWED_HOSTS = [SERVER_IP, SERVER_DOMAIN, f"www.{SERVER_DOMAIN}"]

# Public browser origins — HTTPS only (the whole site forces TLS, so http
# origins would only be dead entries that widen the attack surface).
PUBLIC_ORIGINS = [
    f"https://{SERVER_DOMAIN}",
    f"https://www.{SERVER_DOMAIN}",
]
# Extra SPA / frontend origins: comma-separated, full scheme, via env.
EXTRA_ORIGINS = [o.strip() for o in os.environ.get("CORS_EXTRA_ORIGINS", "").split(",") if o.strip()]

# CSRF
CSRF_TRUSTED_ORIGINS = PUBLIC_ORIGINS + EXTRA_ORIGINS
# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = PUBLIC_ORIGINS + EXTRA_ORIGINS

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
# Ramp: start at 60, confirm HTTPS is solid, then raise to 31536000 (1 year)
# before submitting to the HSTS preload list. Env-tunable so the ramp needs
# no redeploy.
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "60"))
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = True
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# API
# ------------------------------------------------------------------------------
# Drop the browsable API in production — JSON only.
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
)

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
