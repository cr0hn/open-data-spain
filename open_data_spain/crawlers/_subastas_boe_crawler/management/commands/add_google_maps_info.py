from django.core.management.base import BaseCommand

from subastas_boe.models import SubastaBOE
from subastas_boe.sdk.geo_data import add_geo_data


class Command(BaseCommand):
    help = 'Ejecuta el crawler del BOE'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('[*] Starting...'))

        for subasta in SubastaBOE.objects.all():
            add_geo_data(subasta)

        self.stdout.write(self.style.SUCCESS('[*] Done'))
