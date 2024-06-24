from django.urls import path

from . import views

app_name = 'geopolitico-api-v1_0'

urlpatterns = [
    path('comunidades-autonomas/', views.ListAutonomousCommunities.as_view(), name='listas-comunidades-autonomas'),
    path('municipios/<str:codigo_provincia_or_slug>/', views.ListMunicipalities.as_view(), name='listas-localidades'),
    path('provincias/<str:codigo_comunidad_or_slug>/', views.ListProvinces.as_view(), name='listas-provincias'),
]
