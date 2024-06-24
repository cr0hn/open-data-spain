from typing import Callable

import re
import logging

from datetime import date
from urllib.parse import urljoin

from ..helpers import *
from ..constants import *
from ....sdk.net import download_and_parse
from ..complementors import *
from .crawler_tab_processors import *

logger = logging.getLogger("ods")

REGEX_URL_VER = re.compile(r'''(ver=)(\d+)''')


class TabsFinished(Exception):
    ...


# ------------------------------------------------------------------------------------------------------------------
# Listar y descargar subastas
# ------------------------------------------------------------------------------------------------------------------
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


def process_next_tab(pending_tabs: set, shared_data: dict, initial_url: str = None):
    # @lru_cache
    def _get_tab_names_(res) -> set:
        titles = [
            str(x.lower())
            for x in
            res.xpath(".//ul[@class='navlist']/li/a/text()")
        ]

        urls = [
            urljoin(initial_url, x.attrib['href'])
            for x in
            res.xpath(".//ul[@class='navlist']/li/a")
        ]

        return set(zip(titles, urls))

    def get_action(tab_title: str) -> Callable:
        actions = {
            "general": procesar_tab_informacion_general,
            "gestora": procesar_tab_autoridad_gestora,
            "bienes": procesar_tab_bienes,
            "lotes": procesar_tab_lote,
            "relacionados": procesar_tab_acreedor,
            "adicional": procesar_tab_acreedor,
            "pujas": procesar_tab_pujas
        }

        for word, act in actions.items():
            if word in tab_title:
                return act

    if not shared_data:
        response, content = download_and_parse(initial_url)
        pending_tabs.update(
            (x, y)
            for x, y in _get_tab_names_(response)
            if "general" not in x
        )

        get_action("general")(content, response, shared_data)

    else:

        try:
            action, url = pending_tabs.pop()
        except KeyError:
            raise TabsFinished("No hay mas pestañas")
        else:
            response, content = download_and_parse(url)

            get_action(action)(content, response, shared_data)


def crawl_url(url: str) -> dict:
    info = {}

    # La primera pestaña siempre es la misma
    pending_tabs = set()

    try:
        while True:
            process_next_tab(pending_tabs, info, url)

    except TabsFinished:
        # Fin de las pestañas
        ...

    # Añadir información adicional en la que no se ha podido obtener previamente
    logger.debug("Complementando datos de la subasta")
    complementar_datos_subasta(info)

    return info


__all__ = ("crawl_url", "extra_links_subastas")
