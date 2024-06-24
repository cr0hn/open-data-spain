from sdk.regex import REGEX_50_PORCIENTO
from apps.subastas_boe.sdk.constants import SituacionPosesoria


def add_situacion_posesoria(bien: dict, lote: dict, subasta: dict, config) -> bool:
    if bien.get("situacion_posesoria"):
        return False

    if desc := bien.get("descripcion"):

        if REGEX_50_PORCIENTO.search(desc):
            pos = SituacionPosesoria.PORCENTAJE_50
        else:
            pos = SituacionPosesoria.DESCONOCIDO

        bien["situacion_posesoria"] = pos

    return True


__all__ = ("add_situacion_posesoria",)
