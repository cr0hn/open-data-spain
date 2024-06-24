from typing import Iterable

from apps.subastas_boe.sdk.constants import Tasacion, ValorSubasta, PujaMinima, Deposito


def add_valores_totales(bien: dict, lote: dict, subasta: dict, config) -> bool:
    """
    Esta función genera un resumen con los valores totales de la subasta
    """

    def expand_lotes(_subasta: dict) -> Iterable[dict]:
        for _lote in _subasta.get("lotes", []):
            yield _lote.get('informacion_lote', {})

    if subasta.get("tasacion_tipo") == Tasacion.POR_LOTE:
        total_tasacion = sum([lote.get("tasacion", 0) or 0 for lote in expand_lotes(subasta)])
    else:
        total_tasacion = subasta.get("tasacion")

    if subasta.get("valor_subasta_tipo") == ValorSubasta.POR_LOTE:
        total_valor_subasta = sum([lote.get("valor_subasta", 0) or 0 for lote in expand_lotes(subasta)])
    else:
        total_valor_subasta = subasta.get("valor_subasta")

    if subasta.get("puja_minima_tipo") == PujaMinima.POR_LOTE:
        total_puja_minima = sum([lote.get("puja_minima", 0) or 0 for lote in expand_lotes(subasta)])
    else:
        total_puja_minima = subasta.get("puja_minima")

    if subasta.get("deposito_tipo") == Deposito.POR_LOTE:
        total_deposito = sum([lote.get("deposito", 0) or 0 for lote in expand_lotes(subasta)])
    else:
        total_deposito = subasta.get("deposito")

    if "extra" not in subasta:
        subasta["extra"] = {}

    subasta["extra"]["cantidades_totales"] = {
        "tasacion": total_tasacion,
        "valor_subasta": total_valor_subasta,
        "puja_minima": total_puja_minima,
        "deposito": total_deposito
    }

    return True


__all__ = ("add_valores_totales",)
