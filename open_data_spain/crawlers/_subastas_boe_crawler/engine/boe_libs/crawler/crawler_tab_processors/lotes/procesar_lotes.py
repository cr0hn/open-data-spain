import re
import logging

from typing import Dict, List
from urllib.parse import urljoin

import lxml.html

from sdk.xml import xfirst, xtext
from crawlers.subastas_boe_crawler.sdk.net import download_and_parse

from ..utils import *
from ..bienes.aux import aplicar_filtros

from .aux import crear_lote
from .rules_tab_lotes_datos_subasta import RULES_TAB_LOTES_DATOS_SUBASTA

logger = logging.getLogger("ods")

REGEX_URL_LOTE = re.compile(r'''(idLote=)(\d+)''')
REGEX_GET_NUMBERS = re.compile(r'''(\d+)''')


def aux_extraer_informacion_bienes(response) -> List[Dict[str, dict]]:
    """Extrae la información del bin particendo del codigo html.

    Args:
        header_type (str, optional): Tipo de header que se usará para extraer la información. Defaults to "h4". Valid values: "h3", "h4".

    :return: titulo pagina, List[bienes]
    """
    bienes_titles = response.xpath(f".//h4/text()")
    bienes_tables = [lxml.html.tostring(e).decode() for e in response.xpath(".//table")]

    tables_titles = dict(zip(bienes_titles, bienes_tables))

    bienes = []

    for bien_title, bien_table in tables_titles.items():
        bien_informacion = aplicar_filtros(bien_table)
        bien_informacion["cabecera"] = xtext(bien_title)

        bienes.append(bien_informacion)

    return bienes


def extraer_secciones(response):
    page_title = xtext(xfirst(response.xpath("//div[@class='caja']/text()")))

    bienes = None
    informacion_subasta = None

    for title_element in response.xpath("//h3"):
        text = title_element.text_content()
        text_lower = text.lower()

        # Detalles de la subasta
        if "datos relacionados con" in text_lower:
            try:
                table = lxml.html.tostring(title_element.getparent().xpath(".//table")[0])

                informacion_subasta = apply_rules(
                    table,
                    RULES_TAB_LOTES_DATOS_SUBASTA
                )

            except IndexError:
                continue

        # Detalles del bien
        elif "bien" in text_lower:
            base = title_element.getparent()
            bienes = aux_extraer_informacion_bienes(base)

        else:
            continue

    return page_title, informacion_subasta, bienes


def procesar_tab_lote(content: bytes, response, info: dict, pending_lotes: set = None):
    def indice_lote() -> int:
        index = xtext(response.xpath(
            ".//a[@class='current' and starts-with(@id, 'idTabLote')]/text()"
        ))

        return int(index)

    def get_lotes_urls() -> List[str]:
        """Devuelve las URL de los lotes"""
        return [
            urljoin("https://subastas.boe.es/", url.attrib["href"])
            for url in response.xpath(".//ul[@class='navlistver']/*/a[starts-with(@id, 'idTabLote')]")
        ]

    # ----------------------------------------------------------------------------------------------------------------------
    # Varios lotes
    # ----------------------------------------------------------------------------------------------------------------------
    # https://subastas.boe.es/detalleSubasta.php?idSub=SUB-JA-2022-198398&idBus
    # =_eUtucXptTlZXamxGK3BleG1YOVd3OGk0Q0lwK3hmbmlZbFB1K1BGWXpVL29BcTB0Q2xVNnFmWVMyRzNLS1ByWCtiOG9XbThDc09aaDJ5Q2lQdVYrWC9GVW9CcS9tbWdXQWh6RkJNZk5NYmZiMHBvc1IrUnA4THpaUlRMaTM2MmQvQkwzbmdlajJxVVBSbnBNRlVETEpsbERVR1JaSUFWNWNPS1I3elhrNXhQb0JabnZJRXNLaTA5bDhXaXg2Rm9zYTU3dHM0RXRwQkJmazRDZG5NM0xmZFY5NFZwVDdkNTRoY0pWMk1KaWN3UkEzTHBYYk54ODRsUDZrM1pjUm1xSw,,-0-50

    current_lote_index = indice_lote()

    logger.debug(f"    > Procesando lote: {current_lote_index}")

    descripcion_lote, datos_relacionados_subasta, bienes = extraer_secciones(response)

    crear_lote(
        info,
        nombre=f"lote-{current_lote_index}",
        informacion_lote=datos_relacionados_subasta,
        descripcion_lote=descripcion_lote,
        bienes=bienes,
    )

    if current_lote_index == 1:
        pending_lotes = set([
            lote_url
            for lote_url in get_lotes_urls()
            if "idLote=1" not in lote_url
        ])

    try:
        next_lote_url = pending_lotes.pop()
    except KeyError:
        return
    else:
        response, content = download_and_parse(next_lote_url)

        procesar_tab_lote(content, response, info, pending_lotes)
