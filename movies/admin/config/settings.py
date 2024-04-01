"""
For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from split_settings.tools import include

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=str,
)  # set default values and casting

# Инициализация Sentry SDK если есть env SENTRY_DSN
if SENTRY_DSN := os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        enable_tracing=True,
        integrations=[DjangoIntegration()],
        traces_sample_rate=env("TRACES_SAMPLE_RATE", cast=float, default=0.01),
        profiles_sample_rate=env("PROFILES_SAMPLE_RATE", cast=float, default=0.01),
        attach_stacktrace=True,
        send_default_pii=True,
    )

environ.Env.read_env(".env")

include(
    "components/base.py",
    "components/apps.py",
    "components/middlewares.py",
    "components/templates.py",
    "components/databases.py",
    "components/auth.py",
)
