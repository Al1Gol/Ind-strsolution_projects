import datetime
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


# Пользователи
class Users(AbstractUser):
    is_client = models.BooleanField(verbose_name="клиент", default=False)
    is_manager = models.BooleanField(verbose_name="менеджер", default=False)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
        ordering = ["created_at"]


# Федеральные округа
class Districts(models.Model):
    name = models.CharField(verbose_name="полное наименование", max_length=200)

    class Meta:
        verbose_name = "Федеральный округ"
        verbose_name_plural = "Федеральный округ"
        ordering = ["name"]


# Отрасли
class Branches(models.Model):
    name = models.CharField(verbose_name="полное наименование", max_length=200)

    class Meta:
        verbose_name = "Отрасль"
        verbose_name_plural = "Отрасль"
        ordering = ["name"]


# Клиенты
class Clients(models.Model):
    user_id = models.ForeignKey(
        "Users",
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        limit_choices_to={"is_client": True},
    )
    district_id = models.ForeignKey(
        "Districts",
        verbose_name="регион",
        related_name="district_id",
        on_delete=models.PROTECT,
    )
    branch_id = models.ForeignKey(
        "Branches",
        verbose_name="отрасль",
        related_name="branch_id",
        on_delete=models.PROTECT,
    )
    inn = models.CharField(verbose_name="ИНН", max_length=12)
    organization = models.CharField(
        verbose_name="наименование организации", max_length=200
    )

    class Meta:
        verbose_name = "Клиенты"
        verbose_name_plural = "Клиенты"


# Менеджеры
class Managers(models.Model):
    user_id = models.ForeignKey(
        "Users",
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        limit_choices_to={"is_manager": True},
    )
    district_id = models.ManyToManyField(
        "Districts",
        verbose_name="федеральный округ",
        related_name="district",
    )
    branch_id = models.ManyToManyField(
        "Branches",
        verbose_name="отрасль",
        related_name="branch",
    )

    class Meta:
        verbose_name = "Менеджеры"
        verbose_name_plural = "Менеджеры"
