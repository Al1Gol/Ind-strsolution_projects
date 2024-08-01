from django.db import models
from authapp.models import Contracts


# Create your models here.
class Projects(models.Model):
    contract_id = models.ForeignKey(
        "authapp.Contracts",
        verbose_name="договор",
        related_name="tags",
        on_delete=models.CASCADE,
    )
    name = models.CharField(verbose_name="наименование", max_length=1000)
    start_date = models.DateTimeField(
        verbose_name="дата начала",
    )
    deadline = models.DateTimeField(verbose_name="срок выполнения")
    is_completed = models.BooleanField(verbose_name="выполнено", default=False, null=True)
    actual_date = models.DateTimeField(verbose_name="дата фактического выполнения")
    responsible = models.CharField(
        verbose_name="ответственный", max_length=200, blank=True, null=True
    )
    responsible_rp = models.CharField(
        verbose_name="ответственный рп", max_length=200, blank=True, null=True
    )

    class Meta:
        verbose_name = "Проекты"
        verbose_name_plural = "Проекты"