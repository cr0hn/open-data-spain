from django.contrib import messages
from django.shortcuts import render, redirect

from authentication.models import APIKey
from apps.billing.models import Plan

from .forms import CreateAPIKey


# -------------------------------------------------------------------------
# API Keys
# -------------------------------------------------------------------------
def api_keys_list(request):
    api_keys = APIKey.objects.filter(user=request.user)

    return render(request, 'api_keys/apikey_list.html', {'api_keys': api_keys})


def api_keys_create(request):
    user = request.user
    billing_plan: Plan = user.billing_plan
    max_api_keys = billing_plan.plan_features.max_api_keys

    if user.api_keys.count() >= max_api_keys:
        messages.error(request, f'No puedes crear más API Keys. Tu plan solo permite {max_api_keys} API Key.')
        return redirect('dashboard-api-keys:apikey-list')

    if request.method == 'POST':
        form = CreateAPIKey(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()

            messages.success(request, f'API Creada correctamente. API Key: {form.instance.key}')
            return redirect('dashboard-api-keys:apikey-list')

    else:
        form = CreateAPIKey()

    return render(request, 'api_keys/apikey_create.html', {'form': form})


def api_keys_delete(request, pk):
    try:
        api_key = APIKey.objects.get(pk=pk, user=request.user)
    except APIKey.DoesNotExist:
        messages.error(request, 'La API Key no existe')
        return redirect('dashboard-api-keys:apikey-list')

    api_key.delete()

    messages.success(request, 'API Key eliminada correctamente')

    return redirect('dashboard-api-keys:apikey-list')
