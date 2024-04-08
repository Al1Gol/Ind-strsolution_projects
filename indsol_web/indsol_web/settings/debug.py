import os

from .base import *

DEBUG = True

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

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
