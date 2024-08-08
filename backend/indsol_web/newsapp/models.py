from django.db import models

from newsapp.validators import validate_media_extension


# Список новостей
class News(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    text = models.TextField(verbose_name="Текст новости", max_length=40000)
    to_slider = models.BooleanField(verbose_name="Добавить в миниленту", default=False)
    cover = models.ImageField(
        verbose_name="обложка",
        upload_to="news/covers/",
        validators=[validate_media_extension],
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)
    publicated_at = models.DateTimeField(verbose_name="дата публикации")

    def __str__(self):
        return f"{self.id} - {self.title}"

# Список медиа файлов новостей
class Media(models.Model):
    news_id = models.ForeignKey("News", related_name="news", on_delete=models.CASCADE)
    media = models.FileField(
        verbose_name="файлы",
        upload_to="news/media/",
        validators=[validate_media_extension],
    )

    def __str__(self):
        return f"{self.id} - {self.media}"