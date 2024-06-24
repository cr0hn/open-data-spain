import re

from sdk.regex import regex_engine
from sdk.text import text_remove_spaces
from apps.geopolitico.models import Municipio, Provincia
from apps.subastas_boe.sdk.constants import BANCOS_KEYWORDS, TipoAcreedor


REGEX_REMOVE_POSTAL_CODE = re.compile(r'''(\d{4,10})''')


# -------------------------------------------------------------------------
# Información Acreedor
# -------------------------------------------------------------------------
def ac_nombre(html: str) -> dict:
    if found := regex_engine.search("nombre", html):

        ret = {
            "nombre": found.strip(),
            "nombre_raw": found
        }

        # Is a bank?
        _value = found.lower().strip()

        for k, n in BANCOS_KEYWORDS.items():
            if n in _value:
                ret["tipo_acreedor"] = TipoAcreedor.BANCO
                ret["banco"] = k
                break
        else:
            ret["tipo_acreedor"] = TipoAcreedor.OTRO
            ret["banco"] = None

        return ret

    else:

        return {
            "nombre": None,
            "nombre_raw": None,
            "tipo_acreedor": None,
            "banco": None
        }


def ac_nif(html: str) -> dict:
    if found := regex_engine.search("nif", html):
        return {
            "nif": found.strip(),
            "nif_raw": found
        }

    else:
        return {
            "nif": None,
            "nif_raw": None
        }


def ac_direccion(html: str) -> dict:
    if found := regex_engine.search("dirección", html):
        return {
            "direccion": found.strip(),
            "direccion_raw": found
        }

    else:
        return {
            "direccion": None,
            "direccion_raw": None
        }


def ac_municipio(html: str) -> dict or None:
    if found := regex_engine.search("localidad", html):

        step1 = found.lower().strip()

        # Ensure remove postal codes
        step2 = text_remove_spaces(step1).strip()

        if step1 != step2:
            postal_code = REGEX_REMOVE_POSTAL_CODE.search(step1).group(1)
        else:
            postal_code = None

        if geo := Municipio.search(step2):
            municipio = geo.nombre
            codigo_municipio = geo.codigo
        else:
            municipio = None
            codigo_municipio = None

        return {
            "codigo_municipio": codigo_municipio,
            "municipio": municipio,
            "municipio_raw": found,
            "codigo_postal": postal_code
        }
    else:
        return {
            "codigo_municipio": None,
            "municipio": None,
            "codigo_postal": None,
            "municipio_raw": None
        }


def ac_provincia(html: str) -> dict:
    if found := regex_engine.search("provincia", html):

        step1 = found.lower().strip()

        # Ensure remove postal codes
        step2 = text_remove_spaces(step1).strip()

        if step1 != step2:
            postal_code = REGEX_REMOVE_POSTAL_CODE.search(step1).group(1)
        else:
            postal_code = None

        if geo := Provincia.search(step2):
            provincia = geo.nombre
            provincia_codigo = geo.codigo

        else:
            provincia = None
            provincia_codigo = None

        return {
            "provincia": provincia,
            "provincia_raw": found,
            "codigo_provincia": provincia_codigo,
            "codigo_postal": postal_code
        }
    else:
        return {
            "provincia": None,
            "provincia_raw": None,
            "codigo_provincia": None,
            "codigo_postal": None
        }


def ac_pais(html: str) -> dict:
    if found := regex_engine.search("país", html):
        return {
            "pais": found.strip(),
            "pais_raw": found
        }

    else:
        return {
            "pais": None,
            "pais_raw": None
        }


RULES_TAB_ACREEDOR = [
    ac_nombre, ac_nif, ac_direccion, ac_municipio, ac_provincia, ac_pais
]

__all__ = ("RULES_TAB_ACREEDOR",)
