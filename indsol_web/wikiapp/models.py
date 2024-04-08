import datetime

from django.conf import settings
from django.db import models

from .validators import validate_svg_extension, validate_video_extension


class Menu(models.Model):
    name = models.CharField(verbose_name="наименование", max_length=100)
    img = models.FileField(
        verbose_name="иконка",
        validators=[validate_svg_extension],
        upload_to="icons/menu/",
        max_length=100,
        blank=True,
        null=True,
    )
    is_article = models.BooleanField(verbose_name="видимость", default=False)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"
        ordering = ["created_at"]


class Sections(models.Model):
    menu_id = models.ForeignKey(
        "Menu", verbose_name="id меню", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name="раздел", max_length=200)
    img = models.FileField(
        verbose_name="иконка",
        upload_to="icons/sections/",
        validators=[validate_svg_extension],
        max_length=100,
        blank=True,
        null=True,
    )
    is_article = models.BooleanField(verbose_name="видимость", default=False)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Разделы"
        verbose_name_plural = "Разделы"
        ordering = ["created_at"]


class Articles(models.Model):
    menu_id = models.ForeignKey(
        "Menu",
        verbose_name="id меню",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    section_id = models.ForeignKey(
        "Sections",
        verbose_name="id раздел",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    name = models.CharField(verbose_name="наименование статьи", max_length=200)
    text = models.TextField(verbose_name="текст статьи", max_length=100000)
    is_article = models.BooleanField(verbose_name="видимость", default=False)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = "Статьи"
        ordering = ["created_at"]


class Files(models.Model):
    article_id = models.ForeignKey(
        "Articles",
        verbose_name="id статья",
        related_name="files",
        on_delete=models.CASCADE,
    )
    name = models.CharField(verbose_name="название файла", max_length=200)
    file = models.FileField(upload_to="files/", verbose_name="файлы")
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"
        ordering = ["created_at"]


class Images(models.Model):
    img = models.ImageField(
        verbose_name="изображения", upload_to="files/img/", max_length=100
    )

    def __str__(self):
        return self.img

    class Meta:
        verbose_name = "Изображения"
        verbose_name_plural = "Изображения"


class Videos(models.Model):
    video = models.FileField(
        verbose_name="видео",
        upload_to="files/video/",
        max_length=100,
        validators=[validate_video_extension],
    )

    def __str__(self):
        return self.video

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
