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


# Данный метод не работает, так как при каждом сохранении хэширует уже хэшированный пароль
# Из-за этого после превого входа админ не работает
#    def save(self, *args, **kwargs):
#        self.password = make_password(self.password)
#        super(Users, self).save(*args, **kwargs)
