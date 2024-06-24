import re

from typing import Iterable

from sdk.json_tools import find_values_in_dict
from apps.subastas_boe.sdk.constants import TipoConstruccion, TipoPropiedad

# ----------------------------------------------------------------------------------------------------------------------
# Tipo de construcción / Urbano o Rústico
# ----------------------------------------------------------------------------------------------------------------------
REGEX_BUILDING_TYPE = re.compile(r'''(local\s+comercial)''')
REGEX_REMOVE_URBAN_RUSTIC = re.compile(r'(urbana|rustica)(\W+)')


def _ensure_text_in_list(text_list):
    if type(text_list) not in (list, tuple, set):
        t_list = [text_list]
    else:
        t_list = text_list

    return [
        x
        for x in t_list
        if type(x) is str
    ]


def _urbano_or_rustico_(text: Iterable[str], _tipo_construccion: str) -> str:
    if not text:
        return TipoPropiedad.DESCONOCIDO

    fixed_fields = _ensure_text_in_list(text)

    for t in fixed_fields:
        if not t:
            continue

        t_lower = t.lower()

        if any(x in t_lower for x in ("urbana", "urbano")):
            return TipoPropiedad.URBANO

        elif any(x in t_lower for x in ("rústic", "rustic")):
            return TipoPropiedad.RUSTICO

    # If we're in this point not result was found
    if _tipo_construccion_ in (
            TipoConstruccion.SOLAR,
            TipoConstruccion.FINCA_PARCELA
    ):
        return TipoPropiedad.RUSTICO

    elif _tipo_construccion_ in (
            TipoConstruccion.CUADRA,
            TipoConstruccion.PAJAR,
            TipoConstruccion.CASA,
            TipoConstruccion.DUPLEX,
            TipoConstruccion.PISO,
            TipoConstruccion.LOCAL_COMERCIAL,
            TipoConstruccion.GARAGE,
            TipoConstruccion.ALMACEN,
            TipoConstruccion.NAVE,
            TipoConstruccion.TRASTERO,
            TipoConstruccion.OFICINA
    ):
        return TipoPropiedad.URBANO

    else:

        return TipoPropiedad.DESCONOCIDO


def _tipo_construccion_(text: Iterable[str]) -> str:
    if not text:
        return TipoConstruccion.OTHER

    for t in _ensure_text_in_list(text):
        if not t:
            continue

        t_lower = t.lower()

        if any(x in t_lower for x in ("solar",)):
            return TipoConstruccion.SOLAR

        if any(x in t_lower for x in ("unifamiliar", "chalet", "casa")):
            return TipoConstruccion.CASA

        if any(x in t_lower for x in ("duplex",)):
            return TipoConstruccion.DUPLEX

        if any(x in t_lower for x in ("pajar",)):
            return TipoConstruccion.PAJAR

        if any(x in t_lower for x in ("cuadra",)):
            return TipoConstruccion.CUADRA

        if any(x in t_lower for x in ("vivienda", "vivenda", "piso", "departamento")):
            return TipoConstruccion.PISO

        if REGEX_BUILDING_TYPE.search(t_lower) or "local" in t_lower:
            return TipoConstruccion.LOCAL_COMERCIAL

        if any(x in t_lower for x in ("oficina", "despacho")):
            return TipoConstruccion.OFICINA

        if any(x in t_lower for x in ("garage", "garaje", "aparcamiento")):
            return TipoConstruccion.GARAGE

        if any(x in t_lower for x in ("almacen", "almacén", "nave")):
            return TipoConstruccion.ALMACEN

        if any(x in t_lower for x in ("nave",)):
            return TipoConstruccion.NAVE

        if any(x in t_lower for x in ("trastero",)):
            return TipoConstruccion.TRASTERO

        if any(x in t_lower for x in ("parcela", "finca")):
            return TipoConstruccion.FINCA_PARCELA

    return TipoConstruccion.OTHER


# ----------------------------------------------------------------------------------------------------------------------
# Distribución de la vivienda
# ----------------------------------------------------------------------------------------------------------------------
REGEX_CRU_REFERENCE = re.compile(r'(cru)(.*)(\d{14})')
REGEX_REMOVE_SPECIALS = re.compile(r'''([:,./)\-])''')
REGEX_IDUFIR_REFERENCE = re.compile(r'(idufir)(.*)(\d{14})')
REGEX_DISTRIBUCION_HABITACIONES = re.compile(r'(\d{1,2})([\-\s_.]+)(habitaci|dormitor)')
REGEX_DISTRIBUCION_HABITACIONES_TEXT = re.compile(
    r'(un|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)([\-\s_.]+)(habitaci|dormitor)'
)
REGEX_DISTRIBUCION_BANOS = re.compile(r'(\d{0,2})([\-\s_.]+)(baño|baños|aseo)')


def _distribucion_vivienda_(fields: Iterable[str]) -> dict:
    ret = {}

    for e in fields:

        if not e:
            continue

        step1 = REGEX_REMOVE_SPECIALS.sub('', e)
        step2 = step1.lower()

        if "habitacio":
            if found := REGEX_DISTRIBUCION_HABITACIONES.search(step2):
                ret["dormitorios"] = int(found.group(1))

            elif found := REGEX_DISTRIBUCION_HABITACIONES_TEXT.search(step2):
                numbers_map = {
                    "un": 1,
                    "uno": 1,
                    "dos": 2,
                    "tres": 3,
                    "cuatro": 4,
                    "cinco": 5,
                    "seis": 6,
                    "siete": 7,
                    "ocho": 8,
                    "nueve": 9,
                    "diez": 10
                }

                try:
                    dormitorios = numbers_map[found.group(1)]
                    ret["dormitorios"] = dormitorios

                except KeyError:
                    ...

        if found := REGEX_DISTRIBUCION_BANOS.search(step2):
            if found.group(1) != "":
                num_banos = int(found.group(1))

                ret["num-banios"] = num_banos

        if any(x in step2 for x in ("amueblado", "mueble")):
            # TODO
            pass

        if any(x in step2 for x in ("lavadero", "labadero")):
            ret["lavadero"] = 1

        if any(x in step2 for x in ("comedro", "comedor", "salón", "salon")):
            ret["comedor"] = 1

        if "cocina" in step2:
            ret["cocina"] = 1

        if "recibidor" in step2:
            ret["recibidor"] = 1

        if any(x in step2 for x in ("solana", "solarium", "solario")):
            ret["solarium"] = 1

    return ret


def add_bien_detalles(bien: dict, lote: dict, subasta: dict, config) -> bool:

    values = [
        *list(find_values_in_dict(lote, ("descripcion_lote",))),
        *list(find_values_in_dict(bien, ("descripcion", "cabecera")))
    ]

    ### Resolver tipo de contrucción
    if bien.get("tipo_construccion", None):
        return False

    if construccion := _tipo_construccion_(values):
        bien["tipo_construccion"] = construccion
    else:
        bien["tipo_construccion"] = TipoConstruccion.OTHER

    ### Resolver si es urbano o rural


    if urbano_o_rustico := _urbano_or_rustico_(values, construccion):
        bien["tipo_propiedad"] = urbano_o_rustico
    else:
        if bien["tipo_construccion"] in (
                TipoConstruccion.CASA,
                TipoConstruccion.PISO,
                TipoConstruccion.DUPLEX,
                TipoConstruccion.ATICO,
                TipoConstruccion.LOCAL,
                TipoConstruccion.LOCAL_COMERCIAL,
                TipoConstruccion.OFICINA,
                TipoConstruccion.GARAGE,
                TipoConstruccion.ALMACEN,
                TipoConstruccion.TRASTERO
        ):
            bien["tipo_propiedad"] = TipoPropiedad.URBANO

        else:
            bien["TipoPropiedad"] = TipoPropiedad.DESCONOCIDO

    ### Resolver distribución casa: baños, habitaciones, etc
    if distribucion := _distribucion_vivienda_(values):
        bien["distribucion"] = distribucion
    else:
        bien["distribucion"] = {}

    ### Actualizar bien con los nuevos valores
    return True


__all__ = ("add_bien_detalles",)
