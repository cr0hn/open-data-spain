from sdk.regex import regex_engine
from sdk.text import text_parse_price
from subastas_boe.sdk.constants import *


def igc_tramos_pujas_lotes(html: str) -> dict:
    if found := regex_engine.search("tramos", html):

        try:
            tramos_pujas = text_parse_price(found)
            tramos_pujas_tipo = TramosPujas.CON_TRAMOS
        except ValueError:

            _value = found.lower()

            if "sin tramos" in _value:
                tramos_pujas = None
                tramos_pujas_tipo = TramosPujas.SIN_TRAMOS

            else:

                tramos_pujas = None
                tramos_pujas_tipo = TramosPujas.DESCONOCIDO

        return {
            "tramos_pujas": tramos_pujas,
            "tramos_pujas_raw": found,
            "tramos_pujas_tipo": tramos_pujas_tipo
        }

    else:
        return {
            "tramos_pujas": None,
            "tramos_pujas_raw": None,
            "tramos_pujas_tipo": None
        }


def igc_tasacion_lotes(html: str) -> dict:
    if found := regex_engine.search("tasación", html):

        try:
            tasacion = text_parse_price(found)
            tasacion_tipo = Tasacion.CON_TASACION
        except:
            _value = found.lower()

            if "no consta" in _value:
                tasacion_tipo = Tasacion.NO_CONSTA
                tasacion = None

            else:
                tasacion_tipo = Tasacion.DESCONOCIDO
                tasacion = None

        return {
            "tasacion_tipo": tasacion_tipo,
            "tasacion_raw": found,
            "tasacion": tasacion
        }

    else:
        return {
            "tasacion_tipo": None,
            "tasacion_raw": None,
            "tasacion": None
        }


def igc_deposito_lotes(html: str) -> dict:
    if found := regex_engine.search("depósito", html):
        try:
            deposito = text_parse_price(found)
            deposito_tipo = Deposito.NECESARIO
        except ValueError:

            _value = found.lower()

            if "no necesario" in _value:
                deposito_tipo = Deposito.NO_NECESARIO
                deposito = None

            else:
                deposito_tipo = Deposito.DESCONOCIDO
                deposito = None

        return {
            "deposito": deposito,
            "deposito_raw": found,
            "deposito_tipo": deposito_tipo
        }

    else:
        return {
            "deposito": None,
            "deposito_raw": None,
            "deposito_tipo": None
        }


def igc_puja_minima_lotes(html: str) -> dict:
    if found := regex_engine.search("mínima", html):
        try:
            puja_minima = text_parse_price(found)
            puja_minima_tipo = PujaMinima.CON_PUJA_MINIMA
        except ValueError:
            _value = found.lower()

            if "sin puja" in _value:
                puja_minima_tipo = PujaMinima.SIN_PUJA_MINIMA
                puja_minima = None

            elif "no consta" in _value:
                puja_minima_tipo = PujaMinima.NO_CONSTA
                puja_minima = None

            else:

                puja_minima_tipo = PujaMinima.DESCONOCIDO
                puja_minima = None

        return {
            "puja_minima": puja_minima,
            "puja_minima_raw": found,
            "puja_minima_tipo": puja_minima_tipo,
        }

    else:
        return {
            "puja_minima": None,
            "puja_minima_raw": None,
            "puja_minima_tipo": None
        }


RULES_TAB_LOTES_DATOS_RELACIONADOS = (
    igc_tasacion_lotes,
    igc_deposito_lotes,
    igc_puja_minima_lotes,
    igc_tramos_pujas_lotes
)

__all__ = ("RULES_TAB_LOTES_DATOS_RELACIONADOS",)
