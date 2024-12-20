import os

from .base import *

DEBUG = True

CSRF_TRUSTED_ORIGINS = ['http://5.182.4.206:8000', 'http://localhost:3000', 'http://178.237.190.38:8000', 'htpp://178.34.150.253:8000', 'http://194.8.128.75', 'http://194.8.12.75:8000', 'http://185.255.177.7']

#CORS_ALLOWED_ORIGINS = [
#    "http://localhost:3000",
#    "http://192.168.10.107:3000",
#    "http://192.168.10.109:3000",
#    "http://192.168.10.238:5554",
#    "http://192.168.10.172:3000",
#    "http://192.168.10.210:3000",
#    "http://192.168.10.222:3000",
#    "http://192.168.24.82:5554",
#]

# Папка статики
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Время жизни токенов JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
}

# Настройка базы данных
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

# Параметры проксирования
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Настройки планировщика
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # Вывод в консоль
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Отправка по SMTP
EMAIL_HOST = "connect.smtp.bz"
EMAIL_HOST_PASSWORD = "ZJ7PrFSdVTB0"
EMAIL_HOST_USER = "info@ipm-portal.ru"
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'info@ipm-portal.ru'