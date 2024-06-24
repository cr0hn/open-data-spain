import re
import datetime

from sdk.regex import regex_engine
from sdk.text import html_to_text, text_parse_price
from apps.subastas_boe.sdk.constants import TipoFecha, TipoSubasta, ValorSubasta, Tasacion, PujaMinima, TramosPujas, Deposito

REGEX_DATE = re.compile(r'''(iso:\s*)([\-\w:+]+)(\))''', re.IGNORECASE)


def deposito(html: str) -> dict:
    if found := regex_engine.search("importe del depósito", html):
        try:
            deposito_tipo = Deposito.NECESARIO
            deposito = text_parse_price(found)
        except ValueError:

            if "ver importe de consignación de cada lote" in found.lower():
                deposito_tipo = Deposito.POR_LOTE
                deposito = None

            else:

                deposito_tipo = None
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
            "deposito_tipo": Deposito.NO_CONSTA
        }


def tramos_pujas(html: str) -> dict:
    if found := regex_engine.search("Tramos entre pujas", html):
        try:
            tramos_pujas = text_parse_price(html_to_text(found).strip())
            tramos_pujas_tipo = TramosPujas.CON_TRAMOS
        except ValueError:

            _value = found.lower()

            if "cada lote" in _value:
                tramos_pujas = None
                tramos_pujas_tipo = TramosPujas.POR_LOTE

            elif "sin tramos" in _value:
                tramos_pujas = None
                tramos_pujas_tipo = TramosPujas.SIN_TRAMOS

            else:
                tramos_pujas = None
                tramos_pujas_tipo = None

        return {
            "tramos_pujas": tramos_pujas,
            "tramos_pujas_raw": found,
            "tramos_pujas_tipo": tramos_pujas_tipo
        }

    else:
        return {
            "tramos_pujas": None,
            "tramos_pujas_raw": None,
            "tramos_pujas_tipo": TramosPujas.DESCONOCIDO
        }


def puja_minima(html: str) -> dict:
    if found := regex_engine.search("puja mínima", html):
        try:
            puja_minima_tipo = PujaMinima.CON_PUJA_MINIMA
            puja_minima = text_parse_price(found)
        except ValueError:
            _value = found.lower()

            if "sin puja" in _value:
                puja_minima_tipo = PujaMinima.SIN_PUJA_MINIMA
                puja_minima = None

            elif "no consta" in _value:
                puja_minima_tipo = PujaMinima.NO_CONSTA
                puja_minima = None

            elif "cada lote" in _value:
                puja_minima_tipo = PujaMinima.POR_LOTE
                puja_minima = None
            else:

                puja_minima_tipo = None
                puja_minima = None

        return {
            "puja_minima": puja_minima,
            "puja_minima_raw": found,
            "puja_minima_tipo": puja_minima_tipo
        }

    else:
        return {
            "puja_minima": None,
            "puja_minima_raw": None,
            "puja_minima_tipo": PujaMinima.NO_CONSTA
        }


def tasacion(html: str) -> dict:
    if found := regex_engine.search("tasación", html, exact_match=False):
        try:
            tasacion = text_parse_price(found)
            tasacion_tipo = Tasacion.CON_TASACION
        except:
            _value = found.lower()

            if "no consta" in _value:
                tasacion = None
                tasacion_tipo = Tasacion.NO_CONSTA

            elif "cada lote" in _value:
                tasacion = None
                tasacion_tipo = Tasacion.POR_LOTE

            else:
                tasacion = None
                tasacion_tipo = Tasacion.DESCONOCIDO

        return {
            "tasacion": tasacion,
            "tasacion_raw": found,
            "tasacion_tipo": tasacion_tipo
        }

    else:
        return {
            "tasacion": None,
            "tasacion_raw": None,
            "tasacion_tipo": Tasacion.DESCONOCIDO
        }


def valor_subasta(html: str) -> dict:
    if found := regex_engine.search("valor subasta", html):
        _value = html_to_text(found.lower()).strip()

        try:
            valor_subasta = text_parse_price(_value)
            valor_subasta_tipo = ValorSubasta.GENERAL
        except:
            valor_subasta = None

            if "cada lote" in _value:
                valor_subasta_tipo = ValorSubasta.POR_LOTE
            else:
                valor_subasta_tipo = ValorSubasta.DESCONOCIDO

        return {
            "valor_subasta": valor_subasta,
            "valor_subasta_tipo": valor_subasta_tipo,
            "valor_subasta_raw": found
        }

    else:
        return {
            "valor_subasta": None,
            "valor_subasta_tipo": None,
            "valor_subasta_raw": None
        }


def fecha_inicio(html: str) -> dict:
    if found := regex_engine.search("fecha de inicio", html):
        date_string = REGEX_DATE.search(found).group(2)

        return {
            "fecha_inicio": date_string,
            "fecha_inicio_raw": found,
            "tipo_fecha": TipoFecha.FIJADAS
        }

    else:
        return {
            "fecha_inicio": None,
            "fecha_inicio_raw": None,
            "tipo_fecha": TipoFecha.NO_FIJADAS
        }


def fecha_conclusion(html: str) -> dict:
    if found := regex_engine.search("fecha de conclusión", html):
        date_string = REGEX_DATE.search(found).group(2)

        return {
            "fecha_fin": date_string,
            "fecha_fin_raw": found,
            "tipo_fecha": TipoFecha.FIJADAS
        }

    else:
        return {
            "fecha_fin": None,
            "fecha_fin_raw": None,
            "tipo_fecha": TipoFecha.DESCONOCIDO
        }


def identificador(html: str) -> dict:
    if found := regex_engine.search("identificador", html):
        return {
            "identificador": html_to_text(found).strip(),
            "identificador_raw": found
        }

    else:
        return {
            "identificador": None,
            "identificador_raw": None
        }


def tipo_subasta(html: str) -> dict:
    if found := regex_engine.search("tipo de subasta", html):
        _value = html_to_text(found).lower()

        if "tributaria" in _value:
            t = TipoSubasta.HACIENDA
        elif "notarial" in _value:
            t = TipoSubasta.NOTARIAL
        elif "judicial" in _value:
            t = TipoSubasta.JUDICIAL
        else:
            t = TipoSubasta.DESCONOCIDO

        return {
            "tipo_subasta": t,
            "tipo_subasta_raw": found
        }

    else:
        return {
            "tipo_subasta": None,
            "tipo_subasta_raw": None
        }


def cantidad_reclamada(html: str) -> dict:
    if found := regex_engine.search("cantidad reclamada", html):
        return {
            "cantidad_reclamada": text_parse_price(html_to_text(found)),
            "cantidad_reclamada_raw": found
        }

    return {
        "cantidad_reclamada": None,
        "cantidad_reclamada_raw": None
    }


def boe(html: str) -> dict:
    if boe := regex_engine.search("anuncio boe", html):
        return {
            "boe": boe.upper(),
            "boe_raw": boe,
        }
    else:

        return {
            "boe": None,
            "boe_raw": None
        }


RULES_TAB_INFORMACION_GENERAL = [
    boe, cantidad_reclamada, tipo_subasta, identificador, fecha_conclusion, fecha_inicio, valor_subasta, tasacion,
    puja_minima, deposito, tramos_pujas
]

__all__ = (
    "RULES_TAB_INFORMACION_GENERAL",
    # "INFORMACION_GENERAL_MAPPER_RULES_COMPLEX",
    # "make_id"
)
