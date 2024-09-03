from django.db import models
from authapp.models import Clients
from .validators import validate_docs_extension

# Договоры
class Contracts(models.Model):
    client_id = models.ForeignKey(
        "authapp.Clients",
        verbose_name="клиент",
        on_delete=models.CASCADE,
    )
    contract_number = models.CharField(verbose_name="номер договора", max_length=50, unique=True)

    class Meta:
        verbose_name = "Договоры"
        verbose_name_plural = "Договоры"

    def __str__(self):
        return f"{self.id} - {self.contract_number}"
    
# Проекты
class Projects(models.Model):
    contract_id = models.ForeignKey(
        "Contracts",
        verbose_name="договор",
        on_delete=models.CASCADE,
    )
    name = models.CharField(verbose_name="наименование", max_length=1000)
    start_date = models.DateTimeField(
        verbose_name="дата начала",
    )
    deadline = models.DateTimeField(verbose_name="срок выполнения")
    is_completed = models.BooleanField(verbose_name="выполнено", default=False, blank=True)
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

    def __str__(self):
        return f"{self.id} - {self.name}"

# Согласования
class Adjust(models.Model):
    contract_id = models.ForeignKey(
    "Contracts",
    verbose_name="договор",
    on_delete=models.CASCADE,
)
    subject = models.CharField(verbose_name="Объект согласования", max_length=1000)
    sent_date = models.DateTimeField(verbose_name="дата отправки", blank=True, null=True)
    recieve_date = models.DateTimeField(verbose_name="дата получениия", blank=True, null=True)
    is_agreed = models.BooleanField(verbose_name="Согласовано", default=False, blank=True)

    class Meta:
        verbose_name = "Проекты"
        verbose_name_plural = "Проекты"
    
    def __str__(self):
        return f"{self.id} - {self.subject}"
    
#Документы
class Documents(models.Model):
    contract_id = models.ForeignKey(
        "Contracts",
        verbose_name="договор",
        on_delete=models.CASCADE,
    )
    name = models.CharField(verbose_name="Наименование файла", max_length=1000)
    file = models.FileField(
        verbose_name="Документ",
        upload_to="projects/contracts/docs/",
        max_length=1000,
        validators=[validate_docs_extension],)