from django.db import models
from authapp.models import Contracts


# Create your models here.
class Projects(models.Model):
    contracts_id = models.ForeignKey(
        "Contracts",
        verbose_name="договоры",
        on_delete=models.CASCADE,
    )
    name = models.CharField(verbose_name="наименование", max_length=1000)
    start_date = models.DateTimeField(
        verbose_name="дата создания",
    )
    deadline = models.DateTimeField(verbose_name="срок выполнения")
    is_completed = models.BooleanField(verbose_name="выполнено")
    actual_date = models.DateTimeField(verbose_name="дата фактического выполнения")
    responsible = models.CharField(verbose_name="ответственный", max_length=200)
    responsible_rp = models.CharField(verbose_name="ответственный рп", max_length=200)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Проекты"
        verbose_name_plural = "Проекты"
        ordering = ["created_at"]
