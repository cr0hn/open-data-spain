import re
import logging

from datetime import date
from functools import lru_cache
from urllib.parse import urljoin

from crawlers.subastas_boe_crawler.models import SubastaBOE
from crawlers.subastas_boe_crawler.sdk.net import download_and_parse

from ..helpers import *
from ..constants import *

REGEX_URL_VER = re.compile(r'''(ver=)(\d+)''')

logger = logging.getLogger("ods")


# ------------------------------------------------------------------------------------------------------------------
# Listar y descargar subastas
# ------------------------------------------------------------------------------------------------------------------
@lru_cache(128)
def is_subasta_existe(subasta_id: str) -> bool:
    """Devuelve 'True' si ya existe. Falso sino"""

    return SubastaBOE.objects.filter(identificador=subasta_id)


def extra_links_subastas(url: str, ultima_subasta_crawleada: str = None) -> Iterable[str]:
    """
    Descarga la página con el listado de subastas de una provincia y extrae los links a las subastas.

    Lo hace en función de los parámetros de búsqueda. La parsea retorna las url de las subastas
    """
    response, _ = download_and_parse(url)

    valid_years = [str(date.today().year), str(date.today().year - 1)]

    # Guardamos para servir solamente las que no han sido ya crawleadas. Para eso tenemos en cuenta la última
    server_now = False if ultima_subasta_crawleada else True

    for u in response.xpath(".//li[@class='resultado-busqueda']/a/@href")[::-1]:

        # Eliminar las subastas que no sean de este año
        subasta_id = subasta_id_from_url(u)

        if not any(x in subasta_id for x in valid_years):
            continue

        # Buscamos hasta la última subasta que ya hemos crawleado
        if ultima_subasta_crawleada:
            if subasta_id == ultima_subasta_crawleada:
                server_now = True
                continue

            else:
                # Comprobar si ya hemos llegado a la última subasta que hemos procesado
                logger.debug(f"   <II> Saltando subasta {subasta_id} ya crawleada")

        if server_now:
            new_url = urljoin(url, u)

            yield new_url


__all__ = ("extra_links_subastas", "is_subasta_existe")
