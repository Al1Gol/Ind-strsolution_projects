from django.core.exceptions import ValidationError

import os


# Валидатор для загрузки медиа файлов для новостей. Проверяет только расширение файла
def validate_media_extension(value):
    ext = os.path.splitext(value.name)[1]  # возвращает путь+имя файла
    valid_extensions = [".jpg", ".jpeg", ".mp4", ".png"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Поддеживается загрузка только jpg, jpeg и mp4 файлов")
