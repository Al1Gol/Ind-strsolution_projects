import datetime
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    is_client = models.BooleanField(verbose_name="клиент", default=False)
    is_manager = models.BooleanField(verbose_name="менеджер", default=False)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
        ordering = ["created_at"]


class Districts(models.Model):
    name = models.CharField(verbose_name="полное наименование", max_length=200)

    class Meta:
        verbose_name = "Федеральный округ"
        verbose_name_plural = "Федеральный округ"
        ordering = ["name"]


class Branches(models.Model):
    name = models.CharField(verbose_name="полное наименование", max_length=200)

    class Meta:
        verbose_name = "Отрасль"
        verbose_name_plural = "Отрасль"
        ordering = ["name"]


class Clients(models.Model):
    user = models.ForeignKey(
        "Users",
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        limit_choices_to={"is_client": True},
    )
    district_id = models.ForeignKey(
        "Districts",
        verbose_name="регион",
        related_name="регион",
        on_delete=models.PROTECT,
    )
    branch_id = models.ForeignKey(
        "Districts",
        verbose_name="отрасль",
        related_name="отрасль",
        on_delete=models.PROTECT,
    )


class Managers(models.Model):
    user = models.ForeignKey(
        "Users",
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        limit_choices_to={"is_manager": True},
    )
    district_id = models.ManyToManyField(
        "Districts",
        verbose_name="федеральный округ",
        related_name="район",
    )
    branch_id = models.ManyToManyField(
        "Branches",
        verbose_name="отрасль",
        related_name="отрасль",
    )
