from ..utils import *
from .rules_tab_gestora import RULES_TAB_GESTORA


def procesar_tab_autoridad_gestora(content: bytes, response, info: dict):
    info["gestora"] = apply_rules(
        content.decode(),
        RULES_TAB_GESTORA,
    )
