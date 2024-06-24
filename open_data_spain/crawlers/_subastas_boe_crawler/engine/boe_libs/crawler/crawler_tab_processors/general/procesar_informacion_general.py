from urllib.parse import urljoin

from apps.subastas_boe.sdk.constants import OrigenSubasta

from sdk.xml import xfirst

from ..utils import *
from .rules_tab_general import RULES_TAB_INFORMACION_GENERAL


def procesar_tab_informacion_general(content: bytes, response, info: dict):

    info.update(apply_rules(
        content.decode(),
        RULES_TAB_INFORMACION_GENERAL,
    ))

    info["url"] = urljoin(
        "https://subastas.boe.es/",
        xfirst(response.xpath(".//ul[@class='navlist']/li/a")).attrib["href"]
    )
    info["origen"] = OrigenSubasta.BOE

    return response
