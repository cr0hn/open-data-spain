"""
Este fichero contiene las funciones para subir los datos a S3
"""

import logging
import datetime

from functools import lru_cache

from django.db.models import Q
from django.utils.text import slugify

from apps.geopolitico.models import Provincia, ComunidadAutonoma
from sdk.minio import upload_json_to_s3

logger = logging.getLogger("ods")


@lru_cache
def resolver_provincia(provincia: str):
    try:
        return Provincia.objects.filter(Q(nombre__icontains=provincia) | Q(nombre_alternativo__icontains=provincia)).get()
    except Provincia.DoesNotExist:
        return None


@lru_cache
def resolver_comunidad(provincia: str):
    try:
        return ComunidadAutonoma.objects.filter(Q(nombre__icontains=provincia) | Q(nombre_alternativo__icontains=provincia)).get()
    except ComunidadAutonoma.DoesNotExist:
        return None


def upload_to_s3(subasta: dict, provincia: str):

    if not (provincia := resolver_provincia(provincia)):
        logger.warning(f"Provincia no encontrada en base de datos: {provincia}")
        return

    # Format: identificadorSubasta_comunidad_provincia_fecha.json
    file_name = "-".join((
        slugify(provincia.comunidad_autonoma.nombre),
        slugify(provincia.nombre),
        slugify(datetime.datetime.now().strftime("%Y-%m-%d")),
        subasta["identificador"]
    ))

    upload_json_to_s3(f"subastas-boe/{file_name}", subasta)


__all__ = ("upload_to_s3",)
