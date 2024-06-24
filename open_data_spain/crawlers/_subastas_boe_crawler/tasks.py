from celery import shared_task
from django.conf import settings

from .engine.models import *
from .models import SubastaBOE
from .engine.entrypoint import *
from .sdk.geo_data import add_geo_data


@shared_task(name="subastas-boe-add-geo-data")
def task_add_geo_data():

    for subasta in SubastaBOE.objects.all():
        if subasta is None:
            continue

        # add_geo_data(subasta)


@shared_task(name="subastas-boe-crawler")
def procesar_boe_entry():
    tracking.global_max_count = settings.BOE_GLOBAL_MAX_COUNT
    tracking.max_per_territorio = settings.BOE_MAX_PER_TERRITORY

    # Devuelve los bienes procesados uno a uno
    for subasta in procesar_todo_el_boe():

        if subasta is None:
            continue

        # add_geo_data(subasta)
