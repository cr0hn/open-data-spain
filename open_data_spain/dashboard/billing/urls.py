from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'dashboard-billing'

urlpatterns = [
    path('billing/details/', login_required(views.billing_details), name='details'),
    path('billing/suscription/proccess/success/', login_required(views.success_view), name='success'),
    path('billing/suscription/proccess/cancel/', login_required(views.cancel_view), name='cancel'),

    # API
    path('billing/subscription/checkout/', login_required(views.create_checkout_session), name='create-checkout-session'),

    # Webhooks
    path('billing/webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
]
