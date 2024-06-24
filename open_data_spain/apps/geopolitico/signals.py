from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from unidecode import unidecode

from .models import ComunidadAutonoma, Provincia, Municipio


@receiver(post_save, sender=Provincia)
def update_search_vector(sender, instance, **kwargs):
    vector = SearchVector('nombre', weight='A') + SearchVector('nombre_alternativo', weight='B')
    Provincia.objects.filter(pk=instance.pk).update(search_vector=vector)


@receiver(post_save, sender=Municipio)
def update_search_vector(sender, instance, **kwargs):
    vector = SearchVector('nombre', weight='A') + SearchVector('nombre_alternativo', weight='B')
    Municipio.objects.filter(pk=instance.pk).update(search_vector=vector)


@receiver(post_save, sender=ComunidadAutonoma)
def update_search_vector(sender, instance, **kwargs):
    vector = SearchVector('nombre', weight='A') + SearchVector('nombre_alternativo', weight='B')
    ComunidadAutonoma.objects.filter(pk=instance.pk).update(search_vector=vector)
