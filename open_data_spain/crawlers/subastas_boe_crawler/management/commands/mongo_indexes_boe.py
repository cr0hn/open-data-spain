from pymongo import GEO2D
from django.conf import settings
from django.core.management.base import BaseCommand

from sdk.mongodb import mongo_connection


class Command(BaseCommand):
    help = 'Crea los índices de la colección de subastas del BOE'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('[*] Creando índices de la colección de subastas del BOE'))

        cn = mongo_connection()
        col = cn[settings.MONGO_DB][settings.MONGO_COLLECTION_SUBASTAS]

        # Creamos los índices
        col.create_index("subasta_id", unique=True)

        # Crear índice geo-spacial
        col.create_index([("subasta.lotes.bienes.geo_data", GEO2D)])
