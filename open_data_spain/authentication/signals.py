from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from .models import APIKey
from .constants import CACHE_TIMEOUT


@receiver(post_delete, sender=APIKey)
def on_delete_api_key(sender, instance, **kwargs):
    # Lógica de la acción a ejecutar
    # Puedes acceder a los atributos del objeto eliminado a través de `instance`
    # Por ejemplo, puedes realizar otras operaciones relacionadas o enviar notificaciones
    cache.delete(f"api-keys:{instance.key}")


@receiver(post_save, sender=APIKey)
def on_save_api_key(sender, instance, **kwargs):
    cache.set(f"api-keys:{instance.key}", instance.user.serialize(), timeout=CACHE_TIMEOUT)
