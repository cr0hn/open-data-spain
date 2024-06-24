import logging

import lxml.html
import requests

from apps.subastas_boe.sdk.constants import TipoPropiedad

logger = logging.getLogger("ods")


def add_catastro(bien: dict, lote: dict, subasta: dict, config) -> bool:
    """
    Si el catastro es un link al bien, lo descarga y lo añade
    """

    # Buscamos si hay un link al catastro
    catastro_raw: str = bien.get("referencia_catastral_raw", "") or ""

    bien['catastro'] = {}

    if not catastro_raw:
        return False

    # Si no hay link, será con este formato:
    #
    # <a href="consultaDnprc.php?rc=5033504VK4753C0070FR&amp;idSub=SUB-JA-2023-219987" target="_blank" title="Abre datos catastrales en nueva ventana" onclick="return confirm('El Portal de Subastas se va conectar a los servicios web de la Dirección General del Catastro y mostrará la información en una nueva ventana');">5033504VK4753C0070FR</a>
    #
    # Extraemos el link, para que quede así:
    #
    # https://subastas.boe.es/consultaDnprc.php?rc=5033504VK4753C0070FR&idSub=SUB-JA-2023-219987
    #
    ## Extraemos el link
    try:
        rc = catastro_raw.split("rc=")[1].split("&")[0]
    except IndexError:
        logger.error(f"Error al extraer campo 'rc' de la URL de catastro, para el link: {catastro_raw}")
        return False

    try:
        idSub = catastro_raw.split("idSub=")[1].split("\"")[0]
    except IndexError:
        logger.error(f"Error al extraer campo 'idSub' de la URL de catastro, para el link: {catastro_raw}")
        return False

    ## Generamos la URL
    catastro_url = f"https://subastas.boe.es/consultaDnprc.php?rc={rc}&idSub={idSub}"

    try:
        response = requests.get(catastro_url)
    except Exception as e:
        logger.error(f"Error al descargar el catastro desde el BOE en la URL {catastro_url}: {e}")
        return False

    if response.status_code != 200:
        logger.error(f"Error al descargar el catastro desde el BOE en la URL {catastro_url}: {response.status_code}")
        return False

    # Parseamos el HTML
    html = lxml.html.fromstring(response.content)

    ## Buscamos con xpath este elemento: <td headers="h2">PS CEDROS (JJ)-(JJB) 27 Suelo 28680 SAN MARTIN DE VALDEIGLESIAS (MADRID)</td>
    ## Y extraemos el texto
    try:
        localizacion = html.xpath(".//td[@headers='h2']/text()")[0]
    except IndexError:
        logger.error(f"Error al extraer la localización del catastro desde el BOE en la URL {catastro_url}")
        return False

    try:
        tipo_propiedad = html.xpath(".//td[@headers='h3']/text()")[0]

        if "urbano" in tipo_propiedad.lower():
            tipo_propiedad = TipoPropiedad.URBANO
        elif "rústico" in tipo_propiedad.lower() or "rustico" in tipo_propiedad.lower():
            tipo_propiedad = TipoPropiedad.RUSTICO
        else:
            tipo_propiedad = TipoPropiedad.DESCONOCIDO

    except IndexError:
        logger.error(f"Error al extraer el tipo de bien del catastro desde el BOE en la URL {catastro_url}")
        return False

    try:
        uso = html.xpath(".//td[@headers='h4']/text()")[0]
    except IndexError:
        logger.error(f"Error al extraer el uso del catastro desde el BOE en la URL {catastro_url}")
        return False

    try:
        superficie = html.xpath(".//td[@headers='h5']/text()")[0]

        # Limpiar. Ejemplo: "284 m" -> "284" y tipo int
        superficie = int(superficie.split(" ")[0].strip())
    except (IndexError, ValueError):
        logger.error(f"Error al extraer la superficie del catastro desde el BOE en la URL {catastro_url}")
        return False

    try:
        coeficiente_participacion = html.xpath(".//td[@headers='h6']/text()")[0]

        # Limpiar. Ejemplo: "0,000000 %" → "0,000000" y tipo float
        coeficiente_participacion = float(coeficiente_participacion.split(" ")[0].replace(",", ".").replace("%", "").strip())

    except (IndexError, ValueError):
        logger.error(f"Error al extraer el coeficiente de participación del catastro desde el BOE en la URL {catastro_url}")
        coeficiente_participacion = "desconocido"

    try:
        antiguedad = html.xpath(".//td[@headers='h7']/text()")[0]
    except IndexError:
        antiguedad = "desconocido"

    if "extra" not in bien:
        bien["extra"] = {}

    bien['extra']['catastro'] = {
        "localizacion": localizacion,
        "tipo_bien": tipo_propiedad,
        "uso": uso,
        "superficie": superficie,
        "coeficiente_participacion": coeficiente_participacion,
        "antiguedad": antiguedad,
    }

    return True


__all__ = ("add_catastro",)
