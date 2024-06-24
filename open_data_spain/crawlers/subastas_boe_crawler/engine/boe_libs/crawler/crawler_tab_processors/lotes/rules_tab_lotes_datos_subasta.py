from ..general.rules_tab_general import deposito, tramos_pujas, valor_subasta, tasacion, puja_minima, cantidad_reclamada

RULES_TAB_LOTES_DATOS_SUBASTA = (
    cantidad_reclamada,
    valor_subasta,
    tasacion,
    deposito,
    puja_minima,
    tramos_pujas
)


__all__ = ("RULES_TAB_LOTES_DATOS_SUBASTA", )
