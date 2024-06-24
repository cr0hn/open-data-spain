from decimal import Decimal
from typing import Iterable

from django.conf import settings

from .plans import get_plan_features, PlanNames
from .constants import KEY_MAX_REQUESTS_PER_MONTH, KEY_MAX_REQUESTS_PER_MONTH_PREFIX


def current_user_requests_made(user) -> int:
    try:
        return int(settings.REDIS_CONNECTION.get(KEY_MAX_REQUESTS_PER_MONTH.format(user.pk)))
    except TypeError:
        return 0


def all_current_user_requests_made() -> Iterable[tuple[str, int]]:
    """
    Devuelve todas las peticiones realizadas por los usuarios en el mes actual

    :return: Iterable de tuplas (user_pk, requests)
    """

    # Scan redis keys
    for key in settings.REDIS_CONNECTION.scan_iter(f"{KEY_MAX_REQUESTS_PER_MONTH_PREFIX}:*"):
        if ":" not in key:
            continue

        _, user_pk = key.split(":")

        try:
            yield user_pk, int(settings.REDIS_CONNECTION.get(key))
        except TypeError:
            continue


def max_requests_per_month(user) -> int:
    """
    Devuelve el número máximo de peticiones por mes para el usuario

    :param user: Usuario
    :return: Número de peticiones
    """
    features = get_plan_features(user.billing_plan.name)
    return features.get('max_requests_per_month', 0)


def remaining_requests_current_month(user) -> int:
    """
    Calcula las peticiones restantes para el usuario

    :param user: Usuario
    :return: Peticiones restantes o -1 si es ilimitado
    """
    features = get_plan_features(user.billing_plan.name)

    rpm = features.get('max_requests_per_month', 0)

    # Ilimitado
    if rpm == -1:
        return -1
    else:
        return rpm - current_user_requests_made(user)


def calculate_price_current_month(user) -> Decimal | None:
    """
    Calcula el precio de las peticiones realizadas en el mes actual

    :param user: Usuario
    :return: Precio
    """
    plan_name = user.billing_plan.name

    if plan_name != PlanNames.PAY_AS_YOU_GO:
        return None

    features = get_plan_features(plan_name)

    price_per_request = features.get('price_per_request', 0)

    return Decimal(current_user_requests_made(user) * price_per_request)


__all__ = (
    "current_user_requests_made", "remaining_requests_current_month", "max_requests_per_month",
    "calculate_price_current_month", "all_current_user_requests_made"
)
