import os

from .base import *

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Время жизни токенов JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "indsol",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "db",
        "PORT": "5432",
    }
}
