from typing import Iterable, Tuple

from urllib.parse import urlencode, urlunparse

# BASE_URL = "https://subastas.boe.es/subastas_ava.php?campo%5B0%5D=SUBASTA.ORIGEN&dato%5B0%5D=&campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D={" \
#            "tipo_subasta}&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&dato%5B3%5D=&campo%5B4%5D=BIEN.DIRECCION&dato%5B4%5D=&campo%5B5%5D=BIEN" \
#            ".CODPOSTAL&dato%5B5%5D=&campo%5B6%5D=BIEN.LOCALIDAD&dato%5B6%5D=&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D={" \
#            "provincia_id}&campo%5B8%5D=SUBASTA.POSTURA_MINIMA_MINIMA_LOTES&dato%5B8%5D=&campo%5B9%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_1
#            &dato" \
#            "%5B9%5D=&campo%5B10%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_2&dato%5B10%5D=&campo%5B11%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_3&dato
#            %5B11" \
#            "%5D=&campo%5B12%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_4&dato%5B12%5D=&campo%5B13%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_5&dato%5B13%5D" \
#            "=&campo%5B14%5D=SUBASTA.ID_SUBASTA_BUSCAR&dato%5B14%5D=&campo%5B15%5D=SUBASTA.FECHA_FIN_YMD&dato%5B15%5D%5B0%5D=&dato%5B15
#            %5D" \
#            "%5B1%5D=&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=500&sort_field%5B0%5D" \
#            "=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2
#            %5D" \
#            "=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar"
#
# BASE_LOCALIDAD = "https://subastas.boe.es/subastas_ava.php?campo%5B0%5D=SUBASTA.ORIGEN&dato%5B0%5D=&campo%5B1%5D=SUBASTA.AUTORIDAD&dato" \
#                  "%5B1%5D={tipo_subasta}&campo%5B2%5D=SUBASTA.ESTADO&dato%5B2%5D=&campo%5B3%5D=BIEN.TIPO&dato%5B3%5D=&dato%5B4%5D
#                  =&campo" \
#                  "%5B5%5D=BIEN.DIRECCION&dato%5B5%5D=&campo%5B6%5D=BIEN.CODPOSTAL&dato%5B6%5D=&campo%5B7%5D=BIEN.LOCALIDAD&dato%5B7%5D" \
#                  "={localidad}&campo%5B8%5D=BIEN.COD_PROVINCIA&dato%5B8%5D=&campo%5B9%5D=SUBASTA.POSTURA_MINIMA_MINIMA_LOTES&dato%5B9
#                  %5D" \
#                  "=&campo%5B10%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_1&dato%5B10%5D=&campo%5B11%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_2&dato%5B11" \
#                  "%5D=&campo%5B12%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_3&dato%5B12%5D=&campo%5B13%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_4&dato" \
#                  "%5B13%5D=&campo%5B14%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_5&dato%5B14%5D=&campo%5B15%5D=SUBASTA.ID_SUBASTA_BUSCAR&dato
#                  %5B15" \
#                  "%5D=&campo%5B16%5D=SUBASTA.FECHA_FIN_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&campo%5B17%5D=SUBASTA" \
#                  ".FECHA_INICIO_YMD&dato%5B17%5D%5B0%5D=&dato%5B17%5D%5B1%5D=&page_hits=50&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD" \
#                  "&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA" \
#                  ".HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar"

# BASE_LOCALIDAD = "https://subastas.boe.es/subastas_ava.php?campo%5B0%5D=SUBASTA.ORIGEN&dato%5B0%5D=&campo%5B1%5D=SUBASTA.AUTORIDAD&dato" \
#                  "%5B1%5D=&campo%5B2%5D=SUBASTA.ESTADO&dato%5B2%5D={
#                  tipo_subasta}&campo%5B3%5D=BIEN.TIPO&dato%5B3%5D=I&dato%5B4%5D=&campo%5B5%5D=BIEN" \
#                  ".DIRECCION&dato%5B5%5D=&campo%5B6%5D=BIEN.CODPOSTAL&dato%5B6%5D=&campo%5B7%5D=BIEN.LOCALIDAD&dato%5B7%5D=madrid&campo" \
#                  "%5B8%5D=BIEN.COD_PROVINCIA&dato%5B8%5D=&campo%5B9%5D=SUBASTA.POSTURA_MINIMA_MINIMA_LOTES&dato%5B9%5D=&campo%5B10%5D" \
#                  "=SUBASTA.NUM_CUENTA_EXPEDIENTE_1&dato%5B10%5D=&campo%5B11%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_2&dato%5B11%5D=&campo%5B12" \
#                  "%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_3&dato%5B12%5D=&campo%5B13%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_4&dato%5B13%5D=&campo" \
#                  "%5B14%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_5&dato%5B14%5D=&campo%5B15%5D=SUBASTA.ID_SUBASTA_BUSCAR&dato%5B15%5D=&campo
#                  %5B16" \
#                  "%5D=SUBASTA.FECHA_FIN_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&campo%5B17%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B17
#                  %5D" \
#                  "%5B0%5D=&dato%5B17%5D%5B1%5D=&page_hits=50&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field" \
#                  "%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion" \
#                  "=Buscar"
#
# BASE_QUERY_PARAMS = {
#     'campo[0]': 'SUBASTA.ORIGEN',
#     'campo[1]': 'SUBASTA.AUTORIDAD',
#     'campo[2]': 'SUBASTA.ESTADO',
#     'dato[2]': '{tipo_subasta}',
#     'campo[3]': 'BIEN.TIPO',
#     'dato[3]': 'I',
#     'campo[5]': 'BIEN.DIRECCION',
#     'campo[6]': 'BIEN.CODPOSTAL',
#     'campo[7]': 'BIEN.LOCALIDAD',
#     'dato[7]': 'madrid',
#     'campo[8]': 'BIEN.COD_PROVINCIA',
#     'campo[9]': 'SUBASTA.POSTURA_MINIMA_MINIMA_LOTES',
#     'campo[10]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_1',
#     'campo[11]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_2',
#     'campo[12]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_3',
#     'campo[13]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_4',
#     'campo[14]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_5',
#     'campo[15]': 'SUBASTA.ID_SUBASTA_BUSCAR',
#     'campo[16]': 'SUBASTA.FECHA_FIN_YMD',
#     'campo[17]': 'SUBASTA.FECHA_INICIO_YMD',
#     'page_hits': '50',
#     'sort_field[0]': 'SUBASTA.FECHA_FIN_YMD',
#     'sort_order[0]': 'desc',
#     'sort_field[1]': 'SUBASTA.FECHA_FIN_YMD',
#     'sort_order[1]': 'asc',
#     'sort_field[2]': 'SUBASTA.HORA_FIN',
#     'sort_order[2]': 'asc',
#     'accion': 'Buscar'
# }
#
#
# TIPO_SUBASTA = {
#     # Proxima apertura
#     "PU": "Proxima Apertura",
#
#     # Celebrándose
#     "EJ": "Celebrándose"
# }

PROVINCES = {
    "02": "Albacete",
    "03": "Alicante",
    "01": "Álava",  # Está puesto el tercero porque en Álava no hay catastro centralizado. Y para pruebas va peor
    "04": "Almería",
    "05": "Ávila",
    "06": "Badajoz",
    "07": "Baleares",
    "08": "Barcelona",
    "09": "Burgos",
    "10": "Cáceres",
    "11": "Cádiz",
    "12": "Castellón",
    "13": "Ciudad Real",
    "14": "Córdoba",
    "15": "La Coruña",
    "16": "Cuenca",
    "17": "Gerona",
    "18": "Granada",
    "19": "Guadalajara",
    "20": "Guipúzcoa",
    "21": "Huelva",
    "22": "Huesca",
    "23": "Jaén",
    "24": "León",
    "25": "Lérida",
    "26": "La Rioja",
    "27": "Lugo",
    "28": "Madrid",
    "29": "Málaga",
    "30": "Murcia",
    "31": "Navarra",
    "32": "Orense",
    "33": "Asturias",
    "34": "Palencia",
    "35": "Las Palmas",
    "36": "Pontevedra",
    "37": "Salamanca",
    "38": "Santa Cruz de Tenerife",
    "39": "Cantabria",
    "40": "Segovia",
    "41": "Sevilla",
    "42": "Soria",
    "43": "Tarragona",
    "44": "Teruel",
    "45": "Toledo",
    "46": "Valencia",
    "47": "Valladolid",
    "48": "Vizcaya",
    "49": "Zamora",
    "50": "Zaragoza",
    "51": "Ceuta",
    "52": "Melilla"
}

# -------------------------------------------------------------------------
# Provincias a procesar
# -------------------------------------------------------------------------
LOCALIDADES_TO_CRAWL = [
    "madrid",
    "barcelona",
    "valencia",
    "sevilla",
    "malaga",
    "Santa Cruz de Tenerife",
]


def url_subastas_por_provincia() -> Iterable[Tuple[str, str, str]]:
    """
    Enumera las provincias y los tipos de subastas que se pueden.

    :return: (provincia id, tipo_subasta, url)
    :rtype: Iterable[Tuple[str, str, str]]
    """

    schema = 'https'
    host = 'subastas.boe.es'
    path = '/subastas_ava.php'
    base_query_params = {
        'campo[0]': 'SUBASTA.ORIGEN',
        'campo[1]': 'SUBASTA.AUTORIDAD',
        'campo[2]': 'SUBASTA.ESTADO',
        # 'dato[2]': '{tipo_subasta}',  # PU o EJ
        'campo[3]': 'BIEN.TIPO',
        'dato[3]': 'I',
        'campo[5]': 'BIEN.DIRECCION',
        'campo[6]': 'BIEN.CODPOSTAL',
        'campo[7]': 'BIEN.LOCALIDAD',
        # 'dato[7]': 'madrid',
        'campo[8]': 'BIEN.COD_PROVINCIA',
        'campo[9]': 'SUBASTA.POSTURA_MINIMA_MINIMA_LOTES',
        'campo[10]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_1',
        'campo[11]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_2',
        'campo[12]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_3',
        'campo[13]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_4',
        'campo[14]': 'SUBASTA.NUM_CUENTA_EXPEDIENTE_5',
        'campo[15]': 'SUBASTA.ID_SUBASTA_BUSCAR',
        'campo[16]': 'SUBASTA.FECHA_FIN_YMD',
        'campo[17]': 'SUBASTA.FECHA_INICIO_YMD',
        'page_hits': '50',
        'sort_field[0]': 'SUBASTA.FECHA_FIN_YMD',
        'sort_order[0]': 'desc',
        'sort_field[1]': 'SUBASTA.FECHA_FIN_YMD',
        'sort_order[1]': 'asc',
        'sort_field[2]': 'SUBASTA.HORA_FIN',
        'sort_order[2]': 'asc',
        'accion': 'Buscar'
    }

    TIPO_SUBASTA = {
        # Proxima apertura
        "PU": "Proxima Apertura",

        # Celebrándose
        "EJ": "Celebrándose"
    }

    for provincia in LOCALIDADES_TO_CRAWL:
        for tipo_subasta, subasta_name in TIPO_SUBASTA.items():
            query_params = base_query_params.copy()
            query_params['dato[2]'] = tipo_subasta
            query_params['dato[7]'] = provincia

            url = urlunparse((schema, host, path, '', urlencode(query_params), ''))

            # yield province_name, tipo_subasta, f"{province_name} ({subasta_name})", url
            # yield f"{provincia}::{tipo_subasta}", url
            yield provincia, tipo_subasta, url
