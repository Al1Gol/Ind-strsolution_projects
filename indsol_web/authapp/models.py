import datetime
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Regions(models.Model):
    name = models.CharField(verbose_name="название", max_length=100)
    type = models.CharField(verbose_name="тип региона", max_length=20)
    name_with_type = models.CharField(
        verbose_name="полное наименование", max_length=200
    )
    federal_disrtict = models.CharField(verbose_name="федеральный округ")
    kladr_id = models.CharField(verbose_name="кладр", max_length=13)
    flas_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    okato = models.CharField(verbose_name="окато", max_length=12)
    tax_office = models.CharField(verbose_name="налоговая служба", max_length=4)
    postal_code = models.CharField(
        verbose_name="почтовый индекс", max_length=6, blank=True
    )
    iso_code = models.CharField(verbose_name="ISO", max_length=7)
    timezone = models.CharField(verbose_name="часовой пояс", max_length=6)
    geoname_code = models.CharField(verbose_name="код геоимени", max_length=7)
    geoname_id = models.CharField(verbose_name="id геоимени", max_length=7)
    geoname_name = models.CharField(verbose_name="наименование геоимени", max_length=7)


class Users(AbstractUser):
    is_moderate = models.BooleanField(verbose_name="модератор", default=False)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
        ordering = ["created_at"]
