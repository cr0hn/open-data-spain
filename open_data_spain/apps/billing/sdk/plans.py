from typing import List
from dataclasses import dataclass

from django.conf import settings


class PlanNames:
    FREE = 'free'
    PREMIUM = 'premium'
    PROFESSIONAL = 'professional'
    ENTERPRISE = 'enterprise'
    PAY_AS_YOU_GO = 'pay-as-you-go'
    PLAN_NAMES = [
        (FREE, 'Free'),
        (PREMIUM, 'Premium'),
        (PROFESSIONAL, 'Profesional'),
        (ENTERPRISE, 'Enterprise'),
        (PAY_AS_YOU_GO, 'Pago por uso'),
    ]


PLAN_FREE = {
    "max_api_keys": 1,
    "max_concurrent_requests": 1,
    "max_requests_per_minute": 60,
    "max_requests_per_hour": 3_600,
    "max_requests_per_month": 500,
    "available_endpoints": []
}

PLAN_PREMIUM = {
    "max_api_keys": 3,
    "max_concurrent_requests": 2,
    "max_requests_per_minute": 120,
    "max_requests_per_hour": 7_200,
    "max_requests_per_month": 5_000,
    "available_endpoints": []
}

PLAN_PROFESSIONAL = {
    "max_api_keys": 10,
    "max_concurrent_requests": 5,
    "max_requests_per_minute": 300,
    "max_requests_per_hour": 18_000,
    "max_requests_per_month": 20_000,
    "available_endpoints": []
}

PLAN_ENTERPRISE = {
    "max_api_keys": 200,
    "max_concurrent_requests": 25,
    "max_requests_per_minute": 5000,
    "max_requests_per_hour": 300_000,
    "max_requests_per_month": -1,
    "available_endpoints": []
}

DEFAULT_PRICE_PER_REQUEST = 0.009

PAY_AS_YOU_GO = {
    'price_per_request': DEFAULT_PRICE_PER_REQUEST,
    "max_api_keys": 1,
    "max_concurrent_requests": 5,
    "max_requests_per_minute": 300,
    "max_requests_per_hour": 18_000,
    "max_requests_per_month": -1,
    "available_endpoints": []
}


@dataclass
class PlanFeatures:
    """
    Features for a SaaS API as a service
    """
    max_concurrent_requests: int
    max_requests_per_minute: int
    max_requests_per_hour: int
    max_requests_per_month: int

    # The maximum number of API keys that can be created for this plan
    max_api_keys: int

    # The list of endpoints that are available for this plan
    available_endpoints: List[str]


def get_plan_features(plan_name: str) -> dict:
    """
    Get the features for a plan
    """
    plan_map = {
        PlanNames.FREE: PLAN_FREE,
        PlanNames.PREMIUM: PLAN_PREMIUM,
        PlanNames.PROFESSIONAL: PLAN_PROFESSIONAL,
        PlanNames.ENTERPRISE: PLAN_ENTERPRISE,
        PlanNames.PAY_AS_YOU_GO: PAY_AS_YOU_GO,
    }

    try:
        return plan_map[plan_name]
    except KeyError:
        raise ValueError(f"Invalid plan name: {plan_name}")


STRIPE_PLAN_MAPPING_LIVE = {
    "price_1OPWamE8pSFaHKuVpsSD6CtV": PlanNames.FREE,
    "price_1OPWaxE8pSFaHKuVERVI5eao": PlanNames.PREMIUM,
    "price_1OPWasE8pSFaHKuVgTlgiTZ0": PlanNames.PROFESSIONAL,
    "price_1OPWb1E8pSFaHKuVO8WzXMu8": PlanNames.PAY_AS_YOU_GO,
}

STRIPE_PLAN_MAPPING_TEST = {
    "price_1OMu1JE8pSFaHKuVfDoYB8sq": PlanNames.FREE,
    "price_1OMtZrE8pSFaHKuV43pcNivr": PlanNames.PREMIUM,
    "price_1OMtgfE8pSFaHKuVjzKThSHu": PlanNames.PROFESSIONAL,
    "price_1OMX24E8pSFaHKuVrnBZMdyQ": PlanNames.PAY_AS_YOU_GO,
}

STRIPE_PLAN_MAPPING_TEST_NAMES = {
    y: x for x, y in STRIPE_PLAN_MAPPING_TEST.items()
}

STRIPE_PLAN_MAPPING_LIVE_NAMES = {
    y: x for x, y in STRIPE_PLAN_MAPPING_LIVE.items()
}

if settings.DEBUG:
    STRIPE_PLAN_MAPPING_NAMES = STRIPE_PLAN_MAPPING_TEST_NAMES
    STRIPE_PLAN_MAPPING_STRIPE = STRIPE_PLAN_MAPPING_TEST
else:
    STRIPE_PLAN_MAPPING_NAMES = STRIPE_PLAN_MAPPING_LIVE_NAMES
    STRIPE_PLAN_MAPPING_STRIPE = STRIPE_PLAN_MAPPING_LIVE

__all__ = (
    'PlanNames',
    'get_plan_features',
    'PlanFeatures',
    'STRIPE_PLAN_MAPPING_NAMES',
    'STRIPE_PLAN_MAPPING_STRIPE',
    'PLAN_FREE',
    'PLAN_PREMIUM',
    'PLAN_PROFESSIONAL',
)
