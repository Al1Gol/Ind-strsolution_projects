from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(verbose_name="Звголовок", max_length=100)
    text = models.TextField(verbose_name="Текст новости", max_length=40000)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.title}"


class Media(models.Model):
    news_id = models.ForeignKey("News", related_name="news", on_delete=models.CASCADE)
    media = models.FileField(upload_to="news/media", verbose_name="файлы")
