from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy  # <--- Импортируем этот инструмент

class AuthappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authapp"
    verbose_name = "Аутентификация"
    