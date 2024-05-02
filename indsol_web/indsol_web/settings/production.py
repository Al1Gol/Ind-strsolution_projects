import os

from .base import *

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, "static")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "indsol",
        "USER": "postgres",
        "PASSWORD": "123",
        "HOST": "db",
        "PORT": "5432",
    }
}
