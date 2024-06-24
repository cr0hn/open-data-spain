from django.core.management.base import BaseCommand

from crawlers.subastas_boe_crawler.tasks import procesar_boe_entry


class Command(BaseCommand):
    help = 'Ejecuta el crawler del BOE'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('[*] Ejecutando crawler del BOE'))
        procesar_boe_entry()
        self.stdout.write(self.style.SUCCESS('[*] Done'))
