import os
import xml.etree.cElementTree as et

from django.core.exceptions import ValidationError


# Более точный валидатор svg. Не работает из-за with open
# Проверка на SVG
def is_svg(filename):
    tag = None
    with open(filename, "r") as f:
        try:
            for event, el in et.iterparse(f, ("start",)):
                tag = el.tag
                break
        except et.ParseError:
            pass
    return tag == "{http://www.w3.org/2000/svg}svg"


def validate_svg(file):
    if not is_svg(file):
        raise ValidationError("Файл не является svg")


# Валидатор для икононк svg. Проверяет только расширение файла
def validate_svg_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".svg"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Поддеживается загрузка только svg файлов")


# Валидатор для видео. Проверяет только расширение файла
def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".mp4"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            "Поддеживается загрузка только видео файлов с расширением '.mp4'"
        )
