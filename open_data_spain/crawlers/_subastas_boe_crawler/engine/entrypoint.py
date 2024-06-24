import logging

from typing import Iterable

from .models import *
from ..models import SubastaBOE
from .boe_libs.subasta import parsear_subasta
from .boe_libs.helpers import subasta_id_from_url
from .boe_libs.constants import url_subastas_por_provincia
from .boe_libs.crawler import extra_links_subastas, is_subasta_existe
from .boe_libs.s3 import upload_to_s3
from .boe_libs.db_mongo import save_to_mongo

logger = logging.getLogger("ods")


def procesar_todo_el_boe() -> Iterable[SubastaBOE] | None:
    """
    Esta function es el punto de entrada del crawler del BOE.
    """
    logger.info(f") Obteniendo las subastas por cada provincia")

    for provincia, tipo_subasta, url_subastas_provincia in url_subastas_por_provincia():

        # De la página de resultados de los municipios, obtener los links a las subastas
        for url_subasta in extra_links_subastas(url_subastas_provincia, ultima_subasta_crawleada=None):

            subasta_id = subasta_id_from_url(url_subasta)

            # Comprobar que ya hemos procesado esa subasta
            if is_subasta_existe(subasta_id):
                logger.debug(f"   <!> Subasta ya procesada: {subasta_id}")
                continue

            try:
                tracking(provincia)
            except AnalyticMaxPerTerritorio:
                logger.info(f"Alcanza el máximo de subastas procesadas por territorio: {provincia}")
                continue

            except AnalyticMaxGlobal:
                logger.info(f"Alcanza el máximo de subastas procesadas global: {tracking.global_max_count}")
                return

            try:
                # Parsear la subasta
                subasta_dict: dict = parsear_subasta(url_subasta, provincia)

                # Upload to s3
                upload_to_s3(subasta_dict, provincia)

                # Save to postgres
                save_to_mongo(subasta_dict, provincia)

            except Exception as e:
                logger.error(f"Error procesando subasta {subasta_id}: {e}")
                continue


__all__ = ("procesar_todo_el_boe", "parsear_subasta",)
