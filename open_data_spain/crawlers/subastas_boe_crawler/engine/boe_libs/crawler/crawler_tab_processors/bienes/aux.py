from typing import Tuple

import lxml.html

from sdk.xml import xfirst, xtext

from ..utils import *
from .rules_tab_bienes import RULES_TAB_BIENES


def aplicar_filtros(table):
    return apply_rules(
        table,
        RULES_TAB_BIENES
    )


def aux_extraer_informacion_bien(content: bytes, response) -> Tuple[str, list]:
    """Extrae la información del bin particendo del codigo html.

    Args:
        header_type (str, optional): Tipo de header que se usará para extraer la información. Defaults to "h4". Valid values: "h3", "h4".

    :return: titulo pagina, List[bienes]
    """
    page_title = xtext(xfirst(response.xpath("//div[@class='caja']/text()")))
    bienes_titles = response.xpath(f".//h4/text()")
    bienes_tables = [lxml.html.tostring(e).decode() for e in response.xpath(".//table")]

    tables_titles = dict(zip(bienes_titles, bienes_tables))

    bienes = []

    for bien_title, bien_table in tables_titles.items():
        bien_informacion = aplicar_filtros(bien_table)
        bien_informacion["cabecera"] = str(bien_title)

        bienes.append(bien_informacion)

    return page_title, bienes
