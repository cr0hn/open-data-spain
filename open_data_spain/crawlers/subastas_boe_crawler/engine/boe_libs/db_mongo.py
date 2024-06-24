"""
Este fichero contine las funciones necesarias para guardar los datos de las subastas en la base de datos.
"""

import logging

from django.conf import settings
from sdk.mongodb import mongo_connection

logger = logging.getLogger("ods")


def save_to_mongo(subasta: dict):
    cn = mongo_connection()
    col = cn[settings.MONGO_DB][settings.MONGO_COLLECTION_SUBASTAS]

    col.insert_one(subasta)


def find_subasta(subasta_id: str):
    cn = mongo_connection()
    col = cn[settings.MONGO_DB][settings.MONGO_COLLECTION_SUBASTAS]
    return col.find_one({"subasta_id": subasta_id})


__all__ = ("save_to_mongo", "find_subasta")
