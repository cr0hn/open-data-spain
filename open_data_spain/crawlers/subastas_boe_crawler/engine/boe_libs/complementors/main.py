import logging

from .add_bien_id import add_bien_id
from .titles_descriptions import add_titulo
from .bien_detalles import add_bien_detalles
from .add_valores_totales import add_valores_totales
from .situacion_posesoria import add_situacion_posesoria
from .informacion_registral import add_informacion_registral
from .catastro import add_catastro

logger = logging.getLogger("ods")

BIENES_COMPLEMENTS = [
    add_titulo,
    add_informacion_registral,
    add_situacion_posesoria,
    add_bien_detalles,
    add_bien_id,
    add_valores_totales,
    add_catastro,

    # TODO:

    ## Completar con título

    ### Ajustar y poner título descriptivo

    ## Detectar la calidad del inmueble

    ## Descargar fotos

    ### Fotos de catastro

    ### Fotos de Google Maps

    ### Fotos Street View
]


def complementar_datos_subasta(subasta: dict, running_config = None):
    """Procesa un fichero y lo devuelve completado el formato de JSON"""

    returns = []

    for lote in subasta.get("lotes", []):
        for bien in lote.get("bienes", []):
            for fn in BIENES_COMPLEMENTS:

                logger.debug(f"Ejecutando complementador {fn.__name__} for {bien.get('id')} - {bien.get('titulo')}")
                returns.append(fn(bien, lote, subasta, running_config))

    return any(returns)


__all__ = ("complementar_datos_subasta", )
