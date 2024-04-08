from django.apps import AppConfig


class MainappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wikiapp"
    verbose_name = "Главное приложение"
