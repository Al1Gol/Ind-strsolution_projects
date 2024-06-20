import os

from .base import *

DEBUG = True

CSRF_TRUSTED_ORIGINS = ['http://178.237.190.38:8000', 'htpp://178.34.150.253:8000']

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
        "PASSWORD": "7DXCVAEWpxwWsUsBMPmc",
        "HOST": "db",
        "PORT": "5432",
    }
}
