from sdk.xml import xfirst, xtext

from ..lotes.aux import crear_lote
from .aux import aux_extraer_informacion_bien


def procesar_tab_bienes(content: bytes, response, info: dict):
    # ----------------------------------------------------------------------------------------------------------------------
    # Varios inmuebles
    #
    # https://subastas.boe.es/detalleSubasta.php?idSub=SUB-JV-2022-199372&ver=3&idBus
    # =_eUtucXptTlZXamxGK3BleG1YOVd3OGk0Q0lwK3hmbmlZbFB1K1BGWXpVL29BcTB0Q2xVNnFmWVMyRzNLS1ByWCtiOG9XbThDc09aaDJ5Q2lQdVYrWC9GVW9CcS9tbWdXQWh6RkJNZk5NYmZiMHBvc1IrUnA4THpaUlRMaTM2MmQvQkwzbmdlajJxVVBSbnBNRlVETEpsbERVR1JaSUFWNWNPS1I3elhrNXhQb0JabnZJRXNLaTA5bDhXaXg2Rm9zYTU3dHM0RXRwQkJmazRDZG5NM0xmZFY5NFZwVDdkNTRoY0pWMk1KaWN3UkEzTHBYYk54ODRsUDZrM1pjUm1xSw,,-0-200&idLote=&numPagBus=
    # ----------------------------------------------------------------------------------------------------------------------
    nombre_tab = xtext(xfirst(response.xpath(".//a[@class='current']/text()"))).lower()

    #
    # Detectar varios Bienes o no
    #
    #   Si solo existe la pestaña de "bienes" es que solo hay 1 lote
    #   y puede ser procesado de una sola pasada
    if nombre_tab == "bienes":
        page_title, bienes = aux_extraer_informacion_bien(content, response)

        # ------------- ------------------------------------------------------------------------------------------------
        # Crear el lote
        # --------------------------------------------------------------------------------------------------------------
        crear_lote(
            info,
            nombre="lote-1",
            informacion_lote=None,
            descripcion_lote=page_title,
            bienes=bienes
        )
