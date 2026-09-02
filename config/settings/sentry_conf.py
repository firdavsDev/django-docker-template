import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Sentry config — only initialized when a DSN is provided
SENTRY_DSN = os.environ.get("SENTRY_DSN")


def _env_bool(name: str, default: str = "False") -> bool:
    return os.environ.get(name, default).lower() in ("true", "1", "yes")


if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
        ],
        environment=os.environ.get("SENTRY_ENVIRONMENT", "production"),
        release=os.environ.get("SENTRY_RELEASE") or None,
        # Performance tracing off by default — opt in per deployment.
        traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.0")),
        # PII (user emails, IPs, request bodies) off by default — opt in only
        # where privacy policy / GDPR allows.
        send_default_pii=_env_bool("SENTRY_SEND_PII"),
    )
