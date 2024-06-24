from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include, reverse_lazy

urlpatterns = []

if settings.ENABLE_DJANGO_ADMIN:
    urlpatterns.append(
        # Django Admin
        path('c74391f503df4848910c7de0b9779e2f/', admin.site.urls),
    )

if settings.ENABLE_DASHBOARD:
    urlpatterns += [
        # Redirect to dashboard home
        path('', RedirectView.as_view(url=reverse_lazy('dashboard-home:home'), permanent=True)),
        path('', include('dashboard.urls')),

        path("stripe/", include("djstripe.urls", namespace="djstripe")),

        # Allauth
        path('accounts/', include('allauth.urls')),
    ]

if settings.ENABLE_API:
    urlpatterns_api = [
        # End-points
        # path('api/v1.0/user/', include('authentication.api.v1_0.urls')),
        # path('api/v1.0/geo-politico/', include('apps.geopolitico.api.v1_0.urls')),
        path('api/v1.0/subastas-publicas/', include('apps.subastas_boe.api.v1_0.urls')),
    ]
else:
    urlpatterns_api = []

urlpatterns += urlpatterns_api
