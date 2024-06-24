import re

from sdk.text import text_remove_spaces
from sdk.json_tools import find_values_in_dict
from apps.subastas_boe.sdk.constants import OrigenInformacion

REGEX_REFERENCIA_CATASTRAL = re.compile(r'[\w]{20}', re.IGNORECASE)
REGEX_REFERENCIA_CATASTRAL_ALT = re.compile(r'(referencia\s+catastral[:\-]*)([\w\s]+)([.,])', re.IGNORECASE)

REGEX_CRU = re.compile(r'\d{14}', re.IGNORECASE)

REGEX_50_PORCIENTO = re.compile(r'50.*%', re.IGNORECASE)


def add_informacion_registral(bien: dict, lote: dict, subasta: dict, config) -> bool:
    values = list(find_values_in_dict(bien, ("inscripcion_registral", "descripcion", "cabecera")))

    found_rc, found_cru, found_idufir = None, None, None
    found_rc_origin, found_cru_origin, found_idufir_origin = None, None, None

    modified = False

    if not bien.get("cru"):
        for d in values:
            if found := REGEX_CRU.search(d):
                found_cru = found.group()
                found_cru_origin = OrigenInformacion.SCRIPT
                break

    if not bien.get("referencia_catastral"):
        for d in values:
            if found := REGEX_REFERENCIA_CATASTRAL.search(d):
                found_rc = found.group()
                found_rc_origin = OrigenInformacion.SCRIPT
                break

            elif found := REGEX_REFERENCIA_CATASTRAL_ALT.search(d):
                found_rc = text_remove_spaces(found.group(2))
                found_rc_origin = OrigenInformacion.SCRIPT
                break

    if not bien.get("idufir"):
        for d in values:
            if found := REGEX_CRU.search(d):
                found_idufir = found.group()
                found_idufir_origin = OrigenInformacion.SCRIPT
                break

    if found_rc and len(found_rc) == 20:
        bien["referencia_catastral"] = found_rc
        bien["referencia_catastral_origen"] = found_rc_origin

        modified = True

    if found_idufir and len(found_idufir) == 14:
        bien["idufir"] = found_idufir
        bien["idufir_origen"] = found_idufir_origin

        modified = True

    if found_cru and len(found_cru) == 14:
        bien["cru"] = found_cru
        bien["cru_origen"] = found_cru_origin

        modified = True

    return modified


__all__ = ("add_informacion_registral",)
