from django.urls import path


from . import views

app_name = 'subastas-boe-api-v1_0'


urlpatterns = [
    path('boe/hoy/', views.get_subastas_hoy, name='listas-subastas-hoy'),
    path('boe/detalle-subasta/<str:pk>/', views.detalle_subasta, name='detalle-subasta'),

    # path('boe/detalle-bien/<str:pk>/', views.detalle_subasta, name='detalle-bien'),
    #
    # # Búsqueda por comunidad / Provincia
    # path('boe/comunidad/<str:comunidad>/', views.SubastasComunidad.as_view(), name='subastas-por-comunidad'),
    # path('boe/comunidad/<str:comunidad>/provincia/<str:provincia>/', views.SubastasComunidadProvincia.as_view(), name='subastas-por-comunidad-provincia'),
    #
    # # Búsqueda por geolocalización
    # path('boe/geo/', views.SearchGeoLocation.as_view(), name='subastas-geo-location'),
]
