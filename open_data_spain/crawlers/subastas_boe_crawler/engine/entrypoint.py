import logging

from typing import Iterable

from ..models import SubastaBOE

from .analytics import *
from .boe_libs.s3 import upload_to_s3
from .boe_libs.parser import parsear_subasta
from .boe_libs.db_mongo import save_to_mongo, find_subasta
from .boe_libs.constants import url_subastas_por_provincia
from .boe_libs.crawler import crawl_url, extra_links_subastas
from .boe_libs.helpers import subasta_id_from_url, load_json_schema

logger = logging.getLogger("ods")


def is_subasta_existe(subasta_id: str) -> bool:
    """Devuelve 'True' si ya existe. Falso sino"""

    return find_subasta(subasta_id) is not None


def procesar_todo_el_boe(
        max_per_territorio: int = 1000,
        max_global_count: int = 10000,
        log_level: str = "INFO",
) -> Iterable[SubastaBOE] | None:
    """
    Esta function es el punto de entrada del crawler del BOE.
    """
    # -------------------------------------------------------------------------
    # Setup logger
    # -------------------------------------------------------------------------
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

    # -------------------------------------------------------------------------
    # Setup analytics
    # -------------------------------------------------------------------------
    tracking = AnalyticLimits(max_per_territorio, max_global_count)

    # -------------------------------------------------------------------------
    # Cargar JSON Schema
    # -------------------------------------------------------------------------
    json_schema = load_json_schema()

    logger.debug("Obteniendo las subastas por cada provincia")

    for provincia, tipo_subasta, url_subastas_provincia in url_subastas_por_provincia():

        # De la página de resultados de los municipios, obtener los links a las subastas
        for url_subasta in extra_links_subastas(url_subastas_provincia, ultima_subasta_crawleada=None):

            # En este punto tenemos la url de la subasta
            subasta_id = subasta_id_from_url(url_subasta)

            # Comprobar que ya hemos procesado esa subasta
            if is_subasta_existe(subasta_id):
                logger.debug(f"   <!> Subasta ya procesada: {subasta_id}")
                continue

            # -------------------------------------------------------------------------
            # Tracking de las subastas procesadas
            # -------------------------------------------------------------------------
            try:
                tracking(provincia)
            except AnalyticMaxPerTerritorio:
                logger.info(f"Alcanza el máximo de subastas procesadas por territorio: {provincia}")
                continue

            except AnalyticMaxGlobal:
                logger.info(f"Alcanza el máximo de subastas procesadas global: {tracking.global_max_count}")
                return

            # -------------------------------------------------------------------------
            # Crawl de la subasta
            # -------------------------------------------------------------------------
            try:
                logger.debug(f"Crawling subasta {subasta_id}")

                subasta_data: dict = crawl_url(url_subasta)

            except Exception as e:
                logger.error(f"Error haciendo el crawl de la subasta {subasta_id}: {e}")
                continue

            try:
                parsed_subasta: dict = parsear_subasta(subasta_data, provincia=provincia)
            except Exception as e:
                logger.error(f"Error parseando la subasta {subasta_id}: {e}")
                continue

            # -------------------------------------------------------------------------
            # Validar la subasta
            # -------------------------------------------------------------------------
            # try:
            #     json_schema.validate(parsed_subasta)
            # except Exception as e:
            #     logger.error(f"Error validando la subasta {subasta_id}: {e}")
            #     continue

            try:
                upload_to_s3(parsed_subasta, provincia)
            except Exception as e:
                logger.error(f"Error subiendo a S3 la subasta {subasta_id}: {e}")
                ...

            try:
                save_to_mongo(parsed_subasta)
            except Exception as e:
                logger.error(f"Error guardando en MongoDB la subasta {subasta_id}: {e}")
                continue

            logger.info(f"Subasta {subasta_id} procesada correctamente")

            yield parsed_subasta


__all__ = ("procesar_todo_el_boe", "parsear_subasta",)
