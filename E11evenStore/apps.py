from django.apps import AppConfig


class E11evenstoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "E11evenStore"

    def ready(self):
        import E11evenStore.signals
