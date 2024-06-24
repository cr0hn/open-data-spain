from django.conf import settings
from django.shortcuts import render

from apps.billing.sdk.accountability import (
    max_requests_per_month, remaining_requests_current_month, calculate_price_current_month,
    all_current_user_requests_made
)


def home(request):
    plan = request.user.billing_plan
    pending_requests = remaining_requests_current_month(request.user)
    requests_per_month = max_requests_per_month(request.user)
    billing_current_month = calculate_price_current_month(request.user)

    for x in all_current_user_requests_made():
        print(x)

    context = {
        'plan': plan.name,
        'total_api_keys': request.user.api_keys.count(),
        'total_available_api_keys': plan.plan_features.max_api_keys,

        # Estado de la cuenta
        'pending_requests': pending_requests,
        'max_requests_per_month': requests_per_month,
        'billing_current_month': billing_current_month,
    }
    return render(request, 'home/home.html', context)

