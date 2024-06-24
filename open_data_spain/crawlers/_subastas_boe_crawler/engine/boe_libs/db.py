"""
Este fichero contine las funciones necesarias para guardar los datos de las subastas en la base de datos.
"""

import uuid
import logging
import datetime

from functools import lru_cache

# from django.db import IntegrityError, transaction
# from django.db.models import Q
# from django.utils.text import slugify

from sdk.minio import upload_json_to_s3
# from subastas_boe.models import Gestora, Acreedor, Lote, Bien, Subasta
from subastas_boe.models import GestoraBOE, AcreedorBOE, LoteBOE, BienBOE, SubastaBOE
# from geopolitico.models import Provincia, ComunidadAutonoma, Municipio

from .crawler import crawl_url
from .helpers import subasta_id_from_url

logger = logging.getLogger("ods")


def save_to_postgres(subasta: dict, provincia: str):

    # -------------------------------------------------------------------------
    # Creación de los objetos
    # -------------------------------------------------------------------------
    with transaction.atomic():

        #
        ## Comprobamos que no existe ya la subasta
        #
        if Subasta.objects.filter(identificador=subasta["identificador"]).exists():
            logger.warning(f"Subasta {subasta['identificador']} ya existe en la base de datos")
            return

        # Ajustar: fecha_inicio, fecha_fin
        if subasta["fecha_inicio"]:
            fecha_inicio = datetime.datetime.fromisoformat(subasta["fecha_inicio"])
        else:
            fecha_inicio = None

        if subasta["fecha_fin"]:
            fecha_fin = datetime.datetime.fromisoformat(subasta["fecha_fin"])
        else:
            fecha_fin = None

        #
        ## Creamos el gestor
        #
        if gestora := subasta.get("gestora"):
            ## Comprobamos que no existe ya la gestora
            try:
                gestora_obj = Gestora.objects.get(nombre=gestora["codigo"])
            except Gestora.DoesNotExist:
                gestora_obj = Gestora.objects.create(
                    codigo=gestora["codigo"],
                    descripcion=gestora["descripcion"],
                    fax=gestora["fax"],
                    email=gestora["email"],
                    telefono=gestora["telefono"]
                )
        else:
            gestora_obj = None

        #
        ## Creamos el acreedor
        #
        if acreedor := subasta.get("acreedor"):

            try:
                a_mun = acreedor["municipio"].id
            except AttributeError:
                a_mun = None

            try:
                a_pro = acreedor["provincia"].id
            except AttributeError:
                a_pro = None

            acreedor_id = Acreedor.make_key(acreedor['nombre'], acreedor['nif'], a_mun, a_pro, acreedor['direccion'])

            ## Comprobamos que no existe ya el acreedor
            try:
                acreedor_obj = Acreedor.objects.get(pk=acreedor_id)
            except Acreedor.DoesNotExist:
                acreedor_obj, _ = Acreedor.objects.create(
                    codigo=acreedor["codigo"],
                    descripcion=acreedor["descripcion"],
                    fax=acreedor["fax"],
                    email=acreedor["email"],
                    telefono=acreedor["telefono"]
                )

        else:
            acreedor_obj = None

        #
        ## Creamos la subasta
        #
        subasta_obj = Subasta.objects.create(
            identificador=subasta["identificador"],
            url=subasta["url"],
            boe=subasta["boe"],

            origen=subasta["origen"],
            tipo_subasta=subasta["tipo_subasta"],

            fecha_fin=fecha_fin,
            fecha_inicio=fecha_inicio,
            tipo_fecha=subasta["tipo_fecha"],

            cantidad_reclamada=subasta["cantidad_reclamada"],

            valor_subasta=subasta["valor_subasta"],
            valor_subasta_tipo=subasta["valor_subasta_tipo"],

            tasacion=subasta["tasacion"],
            tasacion_tipo=subasta["tasacion_tipo"],

            puja_minima=subasta["puja_minima"],
            puja_minima_tipo=subasta["puja_minima_tipo"],

            deposito=subasta["deposito"],
            deposito_tipo=subasta["deposito_tipo"],

            tramos_pujas=subasta["tramos_pujas"],
            tramos_pujas_tipo=subasta["tramos_pujas_tipo"],

            total_tasacion=subasta["total_tasacion"],
            total_puja_minima=subasta["total_puja_minima"],
            total_deposito=subasta["total_deposito"],
            total_valor_subasta=subasta["total_valor_subasta"],

            gestora=gestora_obj,
            acreedor=acreedor_obj
        )

        #
        ## Creamos los lotes
        #
        for lote in subasta["lotes"]:

            ## Comprobamos que no existe ya el lote
            lote_key = Lote.make_key(subasta_obj.id, lote["nombre"])

            if Lote.objects.filter(pk=lote_key).exists():
                logger.warning(f"Lote {lote['nombre']} ya existe en la base de datos")
                continue

            lote_obj = Lote.objects.create(
                nombre=lote["nombre"],
                descripcion=lote["descripcion"]
            )

            #
            ## Creamos los bienes
            #
            for bien in lote["bienes"]:

                lt_id = Bien.make_key(
                    lote_obj.id,
                    bien["titulo"],
                    bien["cabecera"],
                    bien["tipo_construccion"],
                    bien["tipo_propiedad"],
                    bien["cru"],
                    bien["idufir"],
                    bien["referencia_catastral"]
                )

                ## Comprobamos que no existe ya el bien
                if Bien.objects.filter(pk=lt_id).exists():
                    logger.warning(f"Bien {bien['titulo']} ya existe en la base de datos")
                    continue

                bien_obj = Bien.objects.create(
                    cabecera=bien["cabecera"],
                    titulo=bien["titulo"],
                    descripcion=bien["descripcion"],

                    tamanio=bien["tamanio"],
                    direccion_completa=bien["direccion_completa"],

                    tipo_construccion=bien["tipo_construccion"],
                    tipo_propiedad=bien["tipo_propiedad"],
                    titulo_juridico=bien["titulo_juridico"],

                    situacion_posesoria=bien["situacion_posesoria"],
                    visitable=bien["visitable"],

                    cargas=bien["cargas"],
                    cargas_numero=bien["cargas_numero"],

                    vivienda_habitual=bien["vivienda_habitual"],
                    informacion_adicional=bien["informacion_adicional"],

                    idufir=bien["idufir"],
                    cru=bien["cru"],
                    inscripcion_registral=bien["inscripcion_registral"],
                    referencia_catastral=bien["referencia_catastral"],

                    codigo_postal=bien["codigo_postal"],
                    calle=bien["calle"],

                    lote=lote_obj,
                    municipio=municipio_obj,
                )


__all__ = ("save_to_postgres", )
