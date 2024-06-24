from ..utils import *

from .rules_tab_acreedor import RULES_TAB_ACREEDOR


def procesar_tab_acreedor(content: bytes, response, info: dict):
    info["acreedor"] = apply_rules(
        content.decode(),
        RULES_TAB_ACREEDOR,
    )
