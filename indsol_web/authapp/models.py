import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    is_moderate = models.BooleanField(verbose_name="модератор", default=False)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
        ordering = ["created_at"]
