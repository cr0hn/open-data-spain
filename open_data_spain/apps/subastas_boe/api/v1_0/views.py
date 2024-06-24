import datetime

import orjson
import pymongo
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import authentication_classes

from sdk.views import pagination
from sdk.mongodb import mongo_connection

from .transformations import build_resumen_subasta, build_detalle_subasta


def get_collection() -> pymongo.collection:
    return mongo_connection()[settings.MONGO_DB][settings.MONGO_COLLECTION_SUBASTAS]


@pagination()
def get_subastas_hoy(_request, page, page_size):
    # Get mongo collection
    collection = get_collection()

    # Get subastas from today
    found = collection.find({

        # Publicadas hoy
        'fecha_creacion': {
            '$gte': datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()),
            '$lte': datetime.datetime.combine(datetime.date.today(), datetime.datetime.max.time())
        },

    }).limit(page_size).skip(page_size * (page - 1))

    subasta_results = []
    subasta_append = subasta_results.append

    for total, subasta in enumerate(found, start=1):
        subasta_append(build_resumen_subasta(subasta))
    else:
        total = 0

    ret = {
        'total': total,
        'page': page,
        'page_size': page_size,
        'results': subasta_results
    }

    return JsonResponse(ret, safe=False)


def detalle_subasta(request, pk):
    collection = get_collection()

    # Buscar por _id of identificador
    subasta = collection.find_one({
        '$or': [
            {'_id': pk},
            {'identificador': pk}
        ]}
    )

    if not subasta:
        return JsonResponse({}, safe=False, status=404)

    else:
        return JsonResponse(build_detalle_subasta(subasta), safe=False)
