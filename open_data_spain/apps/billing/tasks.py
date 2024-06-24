from celery.schedules import crontab
from django.conf import settings
from celery_app import app as celery_app

from .models import MonthlyRequestsPerUser
from .sdk import KEY_MAX_REQUESTS_PER_MONTH_PREFIX, all_current_user_requests_made


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Setting up periodic tasks")

    # Ejecutar cada 10 segundos la actualización de los contadores de peticiones
    sender.add_periodic_task(5, update_monthly_requests_usage.s())

    # # Ejecutar cada 1 de cada mes la actualización de los contadores de peticiones. Cada día 1 del mes, a las 00:00
    sender.add_periodic_task(
        crontab(minute=0, hour=0, day_of_month=1),
        reset_counters_for_new_month.s()
    )


@celery_app.task(name="update-monthly-requests-usage")
def update_monthly_requests_usage():
    print("Updating monthly requests usage for all users")

    # Recuperamos todas las peticiones actuales de los usuarios
    for (user_pk, num_request) in all_current_user_requests_made():
        try:
            req, _ = MonthlyRequestsPerUser.objects.get_or_create(
                pk=user_pk,
                user_id=user_pk
            )
            req.requests = num_request
            req.save()

        except Exception as e:
            continue


@celery_app.task(name="reset-counters-for-new-month")
def reset_counters_for_new_month():
    """
    Resetea los contadores de peticiones para el nuevo mes
    """
    print("Resetting counters for new month")

    # Scan redis keys
    for key in settings.REDIS_CONNECTION.scan_iter(f"{KEY_MAX_REQUESTS_PER_MONTH_PREFIX}:*"):
        try:
            settings.REDIS_CONNECTION.set(key, 0)
        except Exception:
            continue
