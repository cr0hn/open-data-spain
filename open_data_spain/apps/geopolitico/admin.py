from django.contrib import admin

from .models import *


@admin.register(ComunidadAutonoma)
class ComunidadAutonomaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "nombre_alternativo")
    search_fields = ("nombre", "nombre_alternativo")


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "nombre_alternativo")
    search_fields = ("nombre", "nombre_alternativo")


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "nombre_alternativo")
    search_fields = ("nombre", "nombre_alternativo")
