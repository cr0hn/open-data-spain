from django.apps import AppConfig


class GeopoliticoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.geopolitico'

    def ready(self):
        import apps.geopolitico.signals
