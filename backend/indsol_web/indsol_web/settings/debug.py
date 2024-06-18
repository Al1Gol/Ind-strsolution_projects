import os

from .base import *

DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, "static")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://192.168.10.107:3000",
    "http://192.168.10.109:3000",
    "http://192.168.10.238:5554",
    "http://192.168.10.172:3000",
    "http://192.168.10.210:3000",
    "http://192.168.10.222:3000",
    "http://192.168.24.82:5554",
]


# Время жизни токенов JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=15),
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "indsol_test",
        "USER": "postgres",
        "PASSWORD": "123",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
