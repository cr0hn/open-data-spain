import uuid
import logging
import datetime

from functools import lru_cache

from django.db import IntegrityError
from django.db.models import Q
from django.utils.text import slugify

from sdk.minio import upload_json_to_s3
from apps.geopolitico.models import Provincia, Municipio, ComunidadAutonoma

from .crawler import crawl_url
from .helpers import subasta_id_from_url

logger = logging.getLogger("ods")


def parsear_subasta(_url_subasta: str, provincia: str) -> dict | None:
    """
    Esta función hace la composición del dato y se asegura de cumplir el formato de la subasta
    """
    # Extraemos el ID de la subasta
    subasta_id = subasta_id_from_url(_url_subasta)

    logger.info(f"Procesando subasta: {subasta_id}")

    boe_data = crawl_url(_url_subasta)

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
    cantidades_totales = boe_data.get("cantidades_totales") or {}

    # De esta manera evitamos que los valores nulos del diccionario sobrescriban los valores por defecto de la BD
    subasta = dict(
        identificador=boe_data["boe"],
        url=boe_data["url"],
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
        # De esta manera evitamos que los valores nulos del diccionario sobrescriban los valores por defecto de la BD
        lote = dict(
            id=uuid.uuid4().hex,
            nombre=lt["nombre"],
            descripcion_lote=lt["descripcion_lote"]
        )

        # El lote tiene información específica de la subasta
        if ifs := lt.get("informacion_subasta"):
            # De esta manera evitamos que los valores nulos del diccionario sobrescriban los valores por defecto de la BD
            informacion_subasta_params = dict(

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

            lote["informacion_subasta"] = informacion_subasta_params

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
            bien_id = uuid.uuid4().hex

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

                referencia_catastral=bien["referencia_catastral"],
                referencia_catastral_raw=bien["referencia_catastral_raw"],
                referencia_catastral_origen=bien["referencia_catastral_origen"],

                codigo_postal=bien["codigo_postal"],
                codigo_postal_raw=bien["codigo_postal_raw"],

                calle=bien["calle"],
                calle_raw=bien["calle_raw"],

                provincia_code=provincia_code,
                provincia_name=provincia_name,
                provincia_slug=provincia_slug,

                municipio_code=municipio_code,
                municipio_name=municipio_name,
                municipio_slug=municipio_slug,

                comunidad_autonoma_code=comunidad_autonoma_code,
                comunidad_autonoma_name=comunidad_autonoma_name,
                comunidad_autonoma_slug=comunidad_autonoma_slug
            )

            total_bienes.append({
                "lote_nombre": lote["nombre"],
                "bien_id": bien_id,
                "extra": bien
            })

            lote["bienes"].append(bien)

        subasta["lotes"].append(lote)

    return subasta
