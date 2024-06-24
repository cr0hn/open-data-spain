from django.apps import AppConfig


class SubastasBoeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subastas_boe'

    def ready(self):
        ...
        # from sdk.mongodb import init_mongo
        # from .models import SubastaBOE
        # init_mongo()
        # SubastaBOE.objects.all()
