from .base import *  # noqa
from .sentry_conf import *  # noqa

SERVER_IP = os.environ["SERVER_IP"]
SERVER_DOMAIN = os.environ["SERVER_DOMAIN"]

DEBUG = os.environ.get("DEBUG", "False") == "True"

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
CORS_ORIGIN_WHITELIST = [
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
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
