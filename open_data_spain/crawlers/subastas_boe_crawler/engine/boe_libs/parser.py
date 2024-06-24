import hashlib
import logging
import datetime
from typing import Tuple

from django.conf import settings
from opencage.geocoder import OpenCageGeocode

from apps.geopolitico.models import Provincia, Municipio, ComunidadAutonoma
from sdk.google_maps import geolocate, GoogleLocation

logger = logging.getLogger("ods")

MAGIC_NUMBER = "d8b26b70a8bc4b258085502e42f79c95"


def make_address(calle: str, municipio: str, provincia: str, comunidad_autonoma) -> str:
    if not calle:
        return ""

    else:
        return ", ".join(x for x in [calle.strip(), municipio, provincia, comunidad_autonoma] if x)


def parsear_subasta(boe_data: dict, provincia: str) -> dict | None:
    """
    Esta función hace la composición del dato y se asegura de cumplir el formato de la subasta
    """

    # Creamos la gestora
    if gst := boe_data.get("gestora"):
        gestora = dict(
            codigo=gst["codigo"],
            descripcion=gst["descripcion"],
            fax=gst["fax"],
            telefono=gst["telefono"],
            email=gst["email"],
        )

    else:
        gestora = None

    # Creamos el acreedor
    if acr := boe_data.get("acreedor"):
        try:
            acr_provincia_obj = Provincia.objects.get(codigo=acr["codigo_provincia"])
            acr_provincia = acr_provincia_obj.codigo
        except Provincia.DoesNotExist:
            logger.error(
                f"Provincia no encontrada para el acreedor ->: "
                f"NIF: {acr['nif']}. "
                f"Codigo Provincia: {acr['codigo_provincia']}. "
                f"Direccion: {acr['direccion']}"
            )

            acr_provincia = None
            acr_provincia_obj = None

        try:
            acr_municipio_obj = Municipio.objects.get(codigo=acr["codigo_municipio"], provincia=acr_provincia_obj)
            acr_municipio = acr_municipio_obj.codigo
        except Municipio.DoesNotExist:
            logger.error(
                f"Municipio no encontrado para el acreedor -> "
                f"NIF: {acr['nif']}. "
                f"Codigo Municipio: {acr['codigo_municipio']}. "
                f"Direccion: {acr['direccion']}"
            )
            acr_municipio = None

        acreedor = dict(
            nif=acr["nif"],
            nombre=acr["nombre"],
            tipo_acreedor=acr["tipo_acreedor"],

            banco=acr.get("banco"),

            direccion=acr["direccion"],
            codigo_postal=acr["codigo_postal"],

            municipio=acr_municipio,
            provincia=acr_provincia,
        )

    else:
        acreedor = None

    # Procesar la subasta
    cantidades_totales = boe_data.get("extra", {}).get("cantidades_totales") or {}

    try:
        provincia_obj = Provincia.objects.get(nombre__icontains=provincia)
        provincia_name = provincia_obj.nombre
        provincia_code = provincia_obj.codigo
        provincia_slug = provincia_obj.nombre_slug

        comunidad_autonoma_obj = provincia_obj.comunidad_autonoma
        comunidad_autonoma_name = comunidad_autonoma_obj.nombre
        comunidad_autonoma_code = comunidad_autonoma_obj.codigo
        comunidad_autonoma_slug = comunidad_autonoma_obj.nombre_slug

    except Provincia.DoesNotExist:
        logger.error(
            f"Provincia no encontrada para la subasta -> "
            f"Provincia: {provincia}"
        )
        provincia_name = provincia_code = provincia_slug = None
        comunidad_autonoma_name = comunidad_autonoma_code = comunidad_autonoma_slug = None

    subasta_url = boe_data.get("url")

    # De esta manera evitamos que los valores nulos del diccionario sobrescriban los valores por defecto de la BD
    subasta = dict(
        identificador=boe_data["boe"],
        url=subasta_url,
        boe=boe_data["boe"],
        origen=boe_data["origen"],

        tipo_subasta=boe_data["tipo_subasta"],
        tipo_subasta_raw=boe_data["tipo_subasta_raw"],

        tipo_fecha=boe_data["tipo_fecha"],

        fecha_inicio=boe_data["fecha_inicio"],
        fecha_inicio_raw=boe_data["fecha_inicio_raw"],

        fecha_fin=boe_data["fecha_fin"],
        fecha_fin_raw=boe_data["fecha_fin_raw"],

        cantidad_reclamada=boe_data["cantidad_reclamada"],
        cantidad_reclamada_raw=boe_data["cantidad_reclamada_raw"],

        valor_subasta=boe_data["valor_subasta"],
        valor_subasta_raw=boe_data["valor_subasta_raw"],
        valor_subasta_tipo=boe_data["valor_subasta_tipo"],

        tasacion=boe_data["tasacion"],
        tasacion_raw=boe_data["tasacion_raw"],
        tasacion_tipo=boe_data["tasacion_tipo"],

        puja_minima=boe_data["puja_minima"],
        puja_minima_raw=boe_data["puja_minima_raw"],
        puja_minima_tipo=boe_data["puja_minima_tipo"],

        deposito=boe_data["deposito"],
        deposito_raw=boe_data["deposito_raw"],
        deposito_tipo=boe_data["deposito_tipo"],

        tramos_pujas=boe_data["tramos_pujas"],
        tramos_pujas_raw=boe_data["tramos_pujas_raw"],
        tramos_pujas_tipo=boe_data["tramos_pujas_tipo"],

        # Cantidades totales
        total_tasacion=cantidades_totales["tasacion"],
        total_puja_minima=cantidades_totales["puja_minima"],
        total_deposito=cantidades_totales["deposito"],
        total_valor_subasta=cantidades_totales["valor_subasta"],

        # Ubicación
        provincia=provincia_name,
        provincia_code=provincia_code,
        provincia_slug=provincia_slug,

        comunidad_autonoma=comunidad_autonoma_name,
        comunidad_autonoma_code=comunidad_autonoma_code,
        comunidad_autonoma_slug=comunidad_autonoma_slug,
    )

    subasta.update({
        "gestora": gestora,
        "acreedor": acreedor,
        "lotes": [],
    })

    total_bienes = []

    #
    # Procesar los lotes
    #
    for lt in boe_data.get("lotes", {}):
        nombre_lote = lt["nombre"]

        # De esta manera evitamos que los valores nulos del diccionario sobrescriban los valores por defecto de la BD
        lote = dict(
            id=hashlib.sha256(f"{MAGIC_NUMBER}#{subasta_url}#lote#{nombre_lote}".encode()).hexdigest(),
            nombre=nombre_lote,
            descripcion_lote=lt["descripcion_lote"]
        )

        # El lote tiene información específica de la subasta
        if ifs := lt.get("informacion_subasta"):
            # De esta manera evitamos que los valores nulos del diccionario sobrescriban los valores por defecto de la BD
            info_subasta_params = dict(

                cantidad_reclamada=ifs["cantidad_reclamada"],
                cantidad_reclamada_raw=ifs["cantidad_reclamada_raw"],

                valor_subasta=ifs["valor_subasta"],
                valor_subasta_raw=ifs["valor_subasta_raw"],
                valor_subasta_tipo=ifs["valor_subasta_tipo"],

                tasacion=ifs["tasacion"],
                tasacion_raw=ifs["tasacion_raw"],
                tasacion_tipo=ifs["tasacion_tipo"],

                puja_minima=ifs["puja_minima"],
                puja_minima_raw=ifs["puja_minima_raw"],
                puja_minima_tipo=ifs["puja_minima_tipo"],

                deposito=ifs["deposito"],
                deposito_raw=ifs["deposito_raw"],
                deposito_tipo=ifs["deposito_tipo"],

                tramos_pujas=ifs["tramos_pujas"],
                tramos_pujas_raw=ifs["tramos_pujas_raw"],
                tramos_pujas_tipo=ifs["tramos_pujas_tipo"]
            )

            lote["subasta_info"] = info_subasta_params

        lote["bienes"] = []

        #
        # Creamos los bienes
        #
        for bien in lt.get("bienes", []):
            try:
                provincia_obj = Provincia.objects.get(codigo=bien["codigo_provincia"])
                provincia_code = provincia_obj.codigo
                provincia_name = provincia_obj.nombre
                provincia_slug = provincia_obj.nombre_slug
            except Provincia.DoesNotExist:
                logger.error(
                    "No se ha encontrado la provincia %s para el bien %s de la subasta %s",
                    bien["codigo_provincia"],
                    bien["titulo"],
                    subasta["identificador"]
                )
                provincia_code = provincia_name = provincia_slug = provincia_obj = None

            try:
                if provincia_obj:
                    municipio_obj = Municipio.objects.get(codigo=bien["codigo_municipio"], provincia=provincia_obj)
                    municipio_code = municipio_obj.codigo
                    municipio_name = municipio_obj.nombre
                    municipio_slug = municipio_obj.nombre_slug
                else:
                    municipio_code = municipio_name = municipio_slug = None

            except Municipio.DoesNotExist:
                logger.error(
                    "No se ha encontrado el municipio %s para el bien %s de la subasta %s",
                    bien["codigo_municipio"],
                    bien["titulo"],
                    subasta["identificador"]
                )
                municipio_code = municipio_name = municipio_slug = None

            try:
                comunidad_autonoma_obj = ComunidadAutonoma.objects.get(codigo=bien["codigo_comunidad_autonoma"])
                comunidad_autonoma_code = comunidad_autonoma_obj.codigo
                comunidad_autonoma_name = comunidad_autonoma_obj.nombre
                comunidad_autonoma_slug = comunidad_autonoma_obj.nombre_slug
            except ComunidadAutonoma.DoesNotExist:
                logger.error(
                    "No se ha encontrado la comunidad autónoma %s para el bien %s de la subasta %s",
                    bien["codigo_comunidad_autonoma"],
                    bien["titulo"],
                    subasta["identificador"]
                )
                comunidad_autonoma_code = comunidad_autonoma_name = comunidad_autonoma_slug = None

            # De esta manera evitamos que los valores nulos del diccionario sobrescriban los valores por defecto de la BD
            bien_id = hashlib.sha256(f"{MAGIC_NUMBER}#{subasta_url}#lote#{nombre_lote}#bien#{bien['titulo']}".encode()).hexdigest()
            bien_catastro = bien.get("extra", {}).get("catastro", {})
            superficie = bien_catastro.get("superficie", "desconocido") or "desconocido"
            address = make_address(bien["calle"], municipio_name, provincia_name, comunidad_autonoma_name)

            # Obtenemos la información geográfica
            geo = geolocate(address, settings.GOOGLE_MAPS_API_KEY)

            if geo:
                geo_data = {
                    "type": "Point",
                    "coordinates": [geo.longitud, geo.latitud]
                }
                geo_raw = geo.to_dict()

            else:
                geo_raw = geo_data = None

            bien = dict(
                id=bien_id,
                cabecera=bien["cabecera"],

                titulo=bien["titulo"],
                descripcion=bien["descripcion"],

                tipo_construccion=bien["tipo_construccion"],
                tipo_propiedad=bien["tipo_propiedad"],

                titulo_juridico=bien["titulo_juridico"],
                titulo_juridico_raw=bien["titulo_juridico_raw"],

                situacion_posesoria=bien["situacion_posesoria"],
                situacion_posesoria_raw=bien["situacion_posesoria_raw"],

                visitable=bien["visitable"],
                visitable_raw=bien["visitable_raw"],

                cargas=bien["cargas"],
                cargas_raw=bien["cargas_raw"],
                cargas_numero=bien["cargas_numero"],

                vivienda_habitual=bien["vivienda_habitual"],
                vivienda_habitual_raw=bien["vivienda_habitual_raw"],

                informacion_adicional=bien["informacion_adicional"],
                informacion_adicional_raw=bien["informacion_adicional_raw"],

                idufir=bien["idufir"],
                idufir_raw=bien["idufir_raw"],
                idufir_origen=bien["idufir_origen"],

                cru=bien["cru"],
                cru_raw=bien["cru_raw"],
                cru_origen=bien["cru_origen"],

                inscripcion_registral=bien["inscripcion_registral"],
                inscripcion_registral_raw=bien["inscripcion_registral_raw"],

                codigo_postal=bien["codigo_postal"],
                codigo_postal_raw=bien["codigo_postal_raw"],

                calle=bien["calle"],
                calle_raw=bien["calle_raw"],

                direccion=address,

                provincia_code=provincia_code,
                provincia_name=provincia_name,
                provincia_slug=provincia_slug,

                municipio_code=municipio_code,
                municipio_name=municipio_name,
                municipio_slug=municipio_slug,

                comunidad_autonoma_code=comunidad_autonoma_code,
                comunidad_autonoma_name=comunidad_autonoma_name,
                comunidad_autonoma_slug=comunidad_autonoma_slug,

                # Catastro
                catastro={
                    "referencia_catastral": bien["referencia_catastral"] or "desconocido",
                    "referencia_catastral_raw": bien["referencia_catastral_raw"] or "desconocido",
                    "referencia_catastral_origen": bien["referencia_catastral_origen"] or "desconocido",
                    "localizacion": bien_catastro.get("localizacion", "desconocido") or "desconocido",
                    "clase": bien_catastro.get("tipo_bien", "desconocido") or "desconocido",
                    "uso": bien_catastro.get("uso", "desconocido") or "desconocido",
                    "coeficiente_participacion": bien_catastro.get("coeficiente_participacion", "desconocido") or "desconocido",
                    "antiguedad": bien_catastro.get("antiguedad", "desconocido") or "desconocido",
                    "superficie": superficie,
                },

                superficie=superficie,

                # Guardamos la información geográfica en formato de MongoDB
                geo_raw=geo_raw,
                geo_data=geo_data,
            )

            total_bienes.append({
                "lote_nombre": lote["nombre"],
                "bien_id": bien_id,
                "extra": bien
            })

            lote["bienes"].append(bien)

        subasta["lotes"].append(lote)

    # Añadir la fecha de creación
    subasta["fecha_creacion"] = datetime.datetime.now()

    return subasta
