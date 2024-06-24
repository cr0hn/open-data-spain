from datetime import datetime

import orjson
import stripe
import stripe.error
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from djstripe.models import Customer
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from .sdk.plans import PlanNames, STRIPE_PLAN_MAPPING_NAMES, STRIPE_PLAN_MAPPING_STRIPE, PLAN_FREE, PLAN_PREMIUM, \
    PLAN_PROFESSIONAL, PAY_AS_YOU_GO


# -------------------------------------------------------------------------
# Billing
# -------------------------------------------------------------------------
def billing_details(request):

    api_keys_per_plan = {
        PlanNames.FREE: PLAN_FREE['max_api_keys'],
        PlanNames.PREMIUM: PLAN_PREMIUM['max_api_keys'],
        PlanNames.PROFESSIONAL: PLAN_PROFESSIONAL['max_api_keys'],
        PlanNames.PAY_AS_YOU_GO: PAY_AS_YOU_GO['max_api_keys'],
    }

    context = {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "api_keys_per_plan": api_keys_per_plan,
    }

    return render(request, 'billing/billing_details.html', context)


def success_view(request):
    messages.success(request, "Suscripción actualizada correctamente.")

    return redirect(reverse('dashboard-billing:details'))


def cancel_view(request):
    messages.error(request, "Suscripción cancelada correctamente.")

    return redirect(reverse('dashboard-billing:details'))


# -------------------------------------------------------------------------
# API
# -------------------------------------------------------------------------
@csrf_exempt
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        data = orjson.loads(request.body)
    except Exception as e:
        return JsonResponse({'error': str(e)})

    # Obtener el plan
    plan = data.get('plan')

    # Comprobar que el plan es válido
    if plan not in STRIPE_PLAN_MAPPING_NAMES.keys():
        return JsonResponse({'error': 'Plan inválido'})

    # Para el plan PAY_AS_YOU_GO, se crea una sesión de checkout con un precio
    line_items = {
        'price': STRIPE_PLAN_MAPPING_NAMES[plan],
    }

    if plan != PlanNames.PAY_AS_YOU_GO:
        line_items['quantity'] = 1

    try:
        session = stripe.checkout.Session.create(
            customer=request.user.stripe_customer.id,
            payment_method_types=["card"],
            line_items=[line_items],
            mode='subscription',
            success_url=request.build_absolute_uri(reverse('dashboard-billing:success')),
            cancel_url=request.build_absolute_uri(reverse('dashboard-billing:cancel')),
        )

        return JsonResponse({"id": session.id})
    except Exception as e:
        # Maneja la excepción
        return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    #
    # Validar el evento
    #
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Firma inválida
        return HttpResponse(status=400)

    #
    # Manejar el evento
    #
    if event['type'] == 'customer.subscription.created':
        session = event['data']['object']

        # Obtener el usuario a partir del id del cliente
        user = Customer.objects.get(id=session['customer']).subscriber

        # Obtener el Plan al que se ha suscrito el usuario
        plan = session['plan']['id']

        # Obtener la expiración de la suscripción
        expiration_date = session['current_period_end']

        # expiration_date -> date
        try:
            date_obj = datetime.fromtimestamp(expiration_date)
        except:
            date_obj = None

        # Cambiar el plan del usuario
        try:
            billing_plan = user.billing
            billing_plan.name = STRIPE_PLAN_MAPPING_STRIPE[plan]
            billing_plan.expiration_date = date_obj
            billing_plan.save()
        except Exception as e:
            return HttpResponse(status=400)

    return HttpResponse(status=200)
