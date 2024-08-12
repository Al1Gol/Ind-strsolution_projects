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
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
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

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # Вывод в консоль
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Отправка по SMTP
EMAIL_HOST = ""
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
