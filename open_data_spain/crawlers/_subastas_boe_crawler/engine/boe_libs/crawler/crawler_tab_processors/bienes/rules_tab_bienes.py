import re
import datetime

from typing import List
from functools import lru_cache

from sdk.text import text_remove_spaces, html_to_text, REGEX_PRICE
from sdk.regex import regex_engine, REGEX_REFERENCIA_CATASTRAL, REGEX_50_PORCIENTO, REGEX_FECHAS

from apps.geopolitico.models import Provincia, ComunidadAutonoma, Municipio
from apps.subastas_boe.sdk.constants import OrigenInformacion, SituacionPosesoria, Visitable, Cargas, TituloJuridico, ViviendaHabitual

# REGEX like:
# - 656.2 LEC
# - 667.2 de la LEC
REGEX_LEYES = re.compile(r'''(\d+(\.\d+)*[\w\s]*lec)|(art\.|articulo|artículo)\s+\d+(\.\d+)*''')
REGEX_TOMOS_LIBROS = re.compile(r'''(tomo|libro|folio|finca\s*(numero|número))\s+\d+''')

REGEX_EXTERNOS_COMUNICACION = re.compile(r'''(registrador[\w\s]*|se)\s*(notificará|notificara|comunicará|comunicara)''')


def _extract_all_prices(text: str) -> List[float]:
    def _is_year(t: str) -> bool:

        @lru_cache
        def _latest_years_() -> List[str]:
            return list(str(x) for x in range(1980, datetime.datetime.now().year))

        if t in _latest_years_():
            return True
        else:
            return False

    def _transform_price(t: str) -> str:

        if t.endswith((".", ",")):
            t = t[:-1]

        # 19.123,23
        if "." in t and "," in t:
            return t.replace(".", "").replace(",", ".")

        # 19.123
        elif "." in t:
            return t.replace(".", "")

        # 19123,23
        elif "," in t:
            return t.replace(",", ".")

        # 19123
        else:
            return t

    if not text:
        return []

    plain_text = html_to_text(text)

    if found := REGEX_PRICE.findall(plain_text):
        ret = []

        for m in found:

            proposal_price = _transform_price(m)

            if _is_year(proposal_price):
                continue

            try:
                ret.append(float(proposal_price))
            except Exception:
                continue

        return ret

    else:
        return []


def b_descripcion(html: str) -> dict:
    if found := regex_engine.search("descripción", html):
        return {
            "descripcion": text_remove_spaces(found.strip()),
            "descripcion_raw": found
        }

    else:
        return {
            "descripcion": None,
            "descripcion_raw": None
        }


def b_idufir(html: str) -> dict:
    if found := regex_engine.search("idufir", html):
        return {
            "idufir": html_to_text(found.strip()),
            "idufir_raw": found,
            "idufir_origen": OrigenInformacion.TAB
        }

    else:
        return {
            "idufir": None,
            "idufir_raw": None,
            "idufir_origen": None
        }


def b_referencia_catastral(html: str) -> dict:
    if found := regex_engine.search("catastral", html, exact_match=False):

        if ref := REGEX_REFERENCIA_CATASTRAL.search(found):
            return {
                "referencia_catastral": ref.group(),
                "referencia_catastral_raw": found,
                "referencia_catastral_origen": OrigenInformacion.TAB
            }
        else:
            return {
                "referencia_catastral": None,
                "referencia_catastral_raw": found,
                "referencia_catastral_origen": OrigenInformacion.TAB
            }

    else:
        return {
            "referencia_catastral": None,
            "referencia_catastral_raw": None,
            "referencia_catastral_origen": None
        }


def b_direccion(html: str) -> dict:
    if found := regex_engine.search("dirección", html):

        return {
            "calle": text_remove_spaces(found.strip()),
            "calle_raw": found
        }

    else:
        return {
            "calle": None,
            "calle_raw": None,
        }


def b_codigo_postal(html: str) -> dict:
    if found := regex_engine.search("postal", html):
        return {
            "codigo_postal": found.lower().strip(),
            "codigo_postal_raw": found
        }

    else:

        return {
            "codigo_postal": None,
            "codigo_postal_raw": None
        }


def b_municipio(html: str) -> dict or None:
    if found := regex_engine.search("localidad", html):

        clean_data = found.lower().strip()

        if geo := Municipio.search(clean_data):
            municipio = geo.nombre
            codigo_municipio = geo.codigo

        else:
            municipio = None
            codigo_municipio = None

        return {
            "municipio": municipio,
            "municipio_raw": found,
            "codigo_municipio": codigo_municipio
        }

    else:
        return {
            "municipio": None,
            "municipio_raw": None,
            "codigo_municipio": None
        }


def b_provincia(html: str) -> dict or None:
    if found := regex_engine.search("provincia", html):

        clean_data = found.lower().strip()

        if geo := Provincia.search(clean_data):
            provincia = geo.nombre
            provincia_codigo = geo.codigo

            if c := ComunidadAutonoma.from_provincia(geo):
                comunidad_autonoma = c.nombre
                codigo_comunidad_autonoma = c.codigo
                comunidad_autonoma_raw = c.nombre

            else:
                comunidad_autonoma = None
                comunidad_autonoma_raw = None
                codigo_comunidad_autonoma = None

        else:
            provincia = None
            provincia_codigo = None
            comunidad_autonoma = None
            comunidad_autonoma_raw = None
            codigo_comunidad_autonoma = None

        return {
            "provincia": provincia,
            "provincia_raw": found,
            "codigo_provincia": provincia_codigo,
            "comunidad_autonoma": comunidad_autonoma,
            "comunidad_autonoma_raw": comunidad_autonoma_raw,
            "codigo_comunidad_autonoma": codigo_comunidad_autonoma

        }
    else:
        return {
            "provincia": None,
            "provincia_raw": None,
            "codigo_provincia": None,
            "comunidad_autonoma": None,
            "comunidad_autonoma_raw": None,
            "codigo_comunidad_autonoma": None
        }


def b_situacion_posesoria(html: str) -> dict or None:
    if found := regex_engine.search("posesoria", html):

        situacion = SituacionPosesoria.DESCONOCIDO

        if clean_data := text_remove_spaces(found).lower().strip():

            if "no consta" in clean_data:
                situacion = SituacionPosesoria.NO_CONSTA

            elif "permanencia" in clean_data:
                situacion = SituacionPosesoria.DERECHO_PERMANENCIA

            elif "desconocido" in clean_data:
                situacion = SituacionPosesoria.OCUPANTE_DESCONOCIDO

            elif "sin ocupantes" in clean_data:
                situacion = SituacionPosesoria.SIN_OCUPANTES

            elif REGEX_50_PORCIENTO.search(clean_data):
                situacion = SituacionPosesoria.PORCENTAJE_50

            else:
                situacion = None

        return {
            "situacion_posesoria": situacion,
            "situacion_posesoria_raw": found,
        }

    else:
        return {
            "situacion_posesoria": None,
            "situacion_posesoria_raw": None
        }


def b_visitable(html: str) -> dict or None:
    if found := regex_engine.search("visitable", html):

        visitable = Visitable.NO_CONSTA

        if clean_data := text_remove_spaces(found).strip().lower():
            if "no consta" in clean_data:
                visitable = Visitable.NO_CONSTA
            elif "no" in clean_data:
                visitable = Visitable.NO
            elif any(x in clean_data for x in ("si", "sí")):
                visitable = Visitable.SI
            else:
                visitable = Visitable.NO_CONSTA

        return {
            "visitable": visitable,
            "visitable_raw": found
        }

    else:
        return {
            "visitable": None,
            "visitable_raw": None
        }


def b_cargas(html: str) -> dict or None:
    if found := regex_engine.search("cargas", html):
        clean_data = found.lower().strip()

        if not clean_data:
            return {
                "cargas": Cargas.SIN_CARGAS,
                "cargas_numero": 0,
                "cargas_raw": found
            }

        cargas_minusculas = text_remove_spaces(clean_data)

        # Detectar cuando apuntan a consultar la web de registradores.org. Ejemplos:
        # - https://subastas.boe.es/detalleSubasta.php?idSub=SUB-JA-2021-183087&ver=3&idBus=&idLote=&numPagBus=
        # - https://subastas.boe.es/detalleSubasta.php?idSub=SUB-JA-2022-192114
        if "registradores.org" in cargas_minusculas:
            return {
                "cargas": Cargas.REGISTRADORES,
                "cargas_numero": 0,
                "cargas_raw": found
            }

        # Eliminar palabras clave, como:
        # - 660 LEC
        # - 656.2 LEC
        cargas_minusculas = REGEX_LEYES.sub("", cargas_minusculas)

        # Eliminar palabras clave, como:
        # - TOMO 761
        # - LIBRO 49
        cargas_minusculas = REGEX_TOMOS_LIBROS.sub("", cargas_minusculas)

        # Eliminar fechas, como:
        # - 21-10-2019
        # - 21/10/2019
        cargas_minusculas = REGEX_FECHAS.sub("", cargas_minusculas)

        if any(x in cargas_minusculas for x in (
                "no tiene", "no consta", "no cargas", "sin cargas"
        )):
            return {
                "cargas": Cargas.SIN_CARGAS,
                "cargas_numero": 0,
                "cargas_raw": found
            }

        cargas = _extract_all_prices(cargas_minusculas)

        # Si no se han extraído precios, es que: o bin hay un error en el parser
        # o bin no consta la cantidad
        if len(cargas) == 0:

            if any(x in cargas_minusculas for x in (
                    "consultar", "segun certifi", "según certi",
                    "se encuentra disponible",
                    "adjunta", "adjunto", "acompaña", "registro de la propiedad",
                    "es posible la consulta", "ver ", "edicto", "certifica",
                    "art. ", " LEC ", "que consten", "que figuren",
                    "a disposición", "a disposicion",
                    "lo dispuesto", "conforme", "consultar", "consultarse"
            )):
                return {
                    "cargas": Cargas.DOCUMENTO_EXTERNO,
                    "cargas_numero": 0,
                    "cargas_raw": found
                }

            elif any(x in cargas_minusculas for x in (
                    "hipoteca",
            )):
                return {
                    "cargas": Cargas.DESCONOCIDO,
                    "cargas_numero": 0,
                    "cargas_raw": found
                }

            elif REGEX_EXTERNOS_COMUNICACION.search(cargas_minusculas):
                return {
                    "cargas": Cargas.DOCUMENTO_EXTERNO,
                    "cargas_numero": 0,
                    "cargas_raw": found
                }

            else:
                return {
                    "cargas": Cargas.SIN_CARGAS,
                    "cargas_numero": 0,
                    "cargas_raw": found
                }

        if len(cargas) == 1:
            try:
                cargas_numero = float(cargas[0])
            except ValueError:
                cargas_numero = 0

            return {
                "cargas": Cargas.CON_CARGAS,
                "cargas_numero": cargas_numero,
                "cargas_raw": found
            }

        # Si tiene más de una carga hay que saber si alguna de ellas es el sumatorio
        # del resto o si hay que sumarlas todas
        max_val = max(cargas)
        cargas_clon = cargas.copy()

        # Eliminamos el valor máximo de la lista
        del cargas_clon[cargas_clon.index(max_val)]

        # Sumamos el resto de cifras para ver si es igual que el máximo
        if sum(cargas_clon) == max_val:

            try:
                cargas_numero = float(max_val)
            except ValueError:
                cargas_numero = 0

            return {
                "cargas": Cargas.CON_CARGAS,
                "cargas_numero": cargas_numero,
                "cargas_raw": found
            }

        else:

            try:
                cargas_numero = sum(cargas)
            except ValueError:
                cargas_numero = 0

            return {
                "cargas": Cargas.CON_CARGAS,
                "cargas_numero": cargas_numero,
                "cargas_raw": found
            }


    else:
        return {
            "cargas": None,
            "cargas_numero": 0,
            "cargas_raw": None
        }


def b_titulo_juridico(html: str) -> dict or None:
    if found := regex_engine.search("jurídico", html):

        if clean_data := found.lower().strip():
            if "pleno" in clean_data:
                titulo = TituloJuridico.PLENO_DOMINIO
            elif "%" in clean_data:
                titulo = TituloJuridico.PARTE
            else:
                titulo = TituloJuridico.DESCONOCIDO

            return {
                "titulo_juridico": titulo,
                "titulo_juridico_raw": found
            }

        else:
            return {
                "titulo_juridico": TituloJuridico.DESCONOCIDO,
                "titulo_juridico_raw": found
            }

    else:
        return {
            "titulo_juridico": None,
            "titulo_juridico_raw": None
        }


def b_informacion_adicional(html: str) -> dict:
    if found := regex_engine.search("adicional", html):
        return {
            "informacion_adicional": found.strip(),
            "informacion_adicional_raw": found
        }

    else:
        return {
            "informacion_adicional": None,
            "informacion_adicional_raw": None
        }


def b_vivienda_habitual(html: str) -> dict:
    if found := regex_engine.search("habitual", html):
        cleaned_data = found.lower().strip()

        if any(x in cleaned_data for x in ("si", "sí")):
            vivienda_habitual = ViviendaHabitual.SI

        elif "no" in cleaned_data:
            vivienda_habitual = ViviendaHabitual.NO

        else:
            vivienda_habitual = ViviendaHabitual.DESCONOCIDO

        return {
            "vivienda_habitual": vivienda_habitual,
            "vivienda_habitual_raw": found
        }

    else:
        return {
            "vivienda_habitual": None,
            "vivienda_habitual_raw": None
        }


def b_inscripcion_registral(html: str) -> dict:
    if found := regex_engine.search("registral", html):
        return {
            "inscripcion_registral": found.strip(),
            "inscripcion_registral_raw": found
        }

    else:
        return {
            "inscripcion_registral": None,
            "inscripcion_registral_raw": None
        }


def b_cru(html: str) -> dict:
    if found := regex_engine.search("cru", html):
        return {
            "cru": found.strip(),
            "cru_raw": found,
            "cru_origen": OrigenInformacion.TAB
        }

    else:
        return {
            "cru": None,
            "cru_raw": None,
            "cru_origen": None
        }


RULES_TAB_BIENES = (
    b_descripcion,
    b_idufir,
    b_referencia_catastral,
    b_direccion,
    b_codigo_postal,
    b_municipio,
    b_provincia,
    b_situacion_posesoria,
    b_visitable,
    b_cargas,
    b_titulo_juridico,
    b_informacion_adicional,
    b_vivienda_habitual,
    b_inscripcion_registral,
    b_cru
)

__all__ = ("RULES_TAB_BIENES",)
