from django.core.management.base import BaseCommand

from subastas_boe.engine.boe_libs.subasta import parsear_subasta


class Command(BaseCommand):
    help = 'Ejecuta el crawler del BOE para una URL'

    # add new parameter: url
    def add_arguments(self, parser):
        parser.add_argument('-u', '--url', type=str, help='URL del BOE')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('[*] Ejecutando crawler del BOE'))
        parsear_subasta(options['url'], None)
        self.stdout.write(self.style.SUCCESS('[*] Done'))
