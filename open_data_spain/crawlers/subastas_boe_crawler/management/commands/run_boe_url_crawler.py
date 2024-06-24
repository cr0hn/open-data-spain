from pprint import pprint

from django.core.management.base import BaseCommand

from crawlers.subastas_boe_crawler.engine.boe_libs import crawl_url
from crawlers.subastas_boe_crawler.engine.boe_libs.parser import parsear_subasta


class Command(BaseCommand):
    help = 'Ejecuta el crawler del BOE para una URL'

    # add new parameter: url
    def add_arguments(self, parser):
        parser.add_argument('boe', type=str, help='número de subasta del BOE')
        # Añadir comunidad autónoma
        parser.add_argument('--comunidad-autonoma', '-c', type=str, help='comunidad autónoma de la subasta', required=True)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('[*] Ejecutando crawler del BOE'))

        url_subasta = f"https://subastas.boe.es/detalleSubasta.php?idSub={options['boe']}"

        try:
            subasta_data: dict = crawl_url(url_subasta)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error haciendo el crawl de la subasta"))
            return

        parsed_subasta: dict = parsear_subasta(subasta_data, options['comunidad_autonoma'])

        pprint(parsed_subasta)
