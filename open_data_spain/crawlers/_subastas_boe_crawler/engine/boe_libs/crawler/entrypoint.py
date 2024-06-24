import logging

from typing import Callable
from urllib.parse import urljoin

from crawlers.subastas_boe_crawler.sdk.net import download_and_parse

from ..complementors import *
from .crawler_tab_processors import *

logger = logging.getLogger("ods")


class TabsFinished(Exception):
    ...


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
    logger.info("Complementando datos de la subasta")
    complementar_datos_subasta(info)

    return info


__all__ = ("crawl_url",)
