from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiResponse, extend_schema

from dashboard.api_keys.authentication import TokenAuthentication
from apps.geopolitico.models import ComunidadAutonoma, Provincia, Municipio

from .openapi import *


class ListAutonomousCommunities(APIView):
    """Devuelve la lista de comunidades autónomas."""

    authentication_classes = [TokenAuthentication]

    @extend_schema(
        operation_id="Listar comunidades autónomas",
        tags=['geo-politico'],
        description="""Obtiene la lista de comunidades autónomas""",
        responses={
            200: OpenApiResponse(
                response=ListAutonomousCommunitiesSchema,
                description="Lista de comunidades autónomas",
            ),
            401: OpenApiResponse(
                response=ErrorSchema,
                description="No autorizado",
            )
        }
    )
    def get(self, request):
        return JsonResponse([
            {
                "codigo": comunidad.codigo,
                "nombre": comunidad.nombre,
                "nombre_slug": comunidad.nombre_slug,
                "nombre_alternativo": comunidad.nombre_alternativo,
                "nombre_alternativo_slug": comunidad.nombre_alternativo_slug
            }
            for comunidad in ComunidadAutonoma.objects.all()
        ], safe=False)


class ListProvinces(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        operation_id="Listar provincias",
        tags=['geo-politico'],
        description="""Obtiene la lista de provincias de una comunidad autónoma a partir de su código o nombre slug.

El slug es el nombre de la comunidad autónoma en minúsculas, sin espacios y sin caracteres especiales. 

Por ejemplo, para la comunidad autónoma de Castilla y León, el slug sería "castilla-y-leon.""",
        responses={
            200: OpenApiResponse(
                response=ListProvincesSchema,
                description="Lista de comunidades autónomas",
            ),
            204: OpenApiResponse(
                response=ErrorSchema,
                description="No encontrado",
            ),
            401: OpenApiResponse(
                response=ErrorSchema,
                description="No autorizado",
            )
        }
    )
    def get(self, request, codigo_comunidad_or_slug):

        try:
            return JsonResponse([
                {
                    "codigo": provincia.codigo,
                    "nombre": provincia.nombre,
                    "nombre_slug": provincia.nombre_slug,
                    "nombre_alternativo": provincia.nombre_alternativo,
                    "nombre_alternativo_slug": provincia.nombre_alternativo_slug
                }

                # Buscar en el codigo, nombre slug, nombre alternativo slug
                for provincia in Provincia.objects.prefetch_related('comunidad_autonoma').filter(
                    Q(comunidad_autonoma__codigo=codigo_comunidad_or_slug) |
                    Q(comunidad_autonoma__nombre_slug=codigo_comunidad_or_slug) |
                    Q(comunidad_autonoma__nombre_alternativo_slug=codigo_comunidad_or_slug)
                )
            ], safe=False)

        except ComunidadAutonoma.DoesNotExist:
            return JsonResponse({"error": "La comunidad autónoma no existe."})


class ListMunicipalities(APIView):

    @extend_schema(
        operation_id="Listar municipios",
        tags=['geo-politico'],
        description="""
Obtiene la lista de municipios de una provincia.

El slug es el nombre de la provincia en minúsculas, sin espacios y sin caracteres especiales.

Por ejemplo, para la provincia de Las Palmas, el slug sería "las-palmas".
""",
        responses={
            200: OpenApiResponse(
                response=ListMunicipalitiesSchema,
                description="Lista de comunidades autónomas",
            ),
            204: OpenApiResponse(
                response=ErrorSchema,
                description="No encontrado"
            ),
            401: OpenApiResponse(
                response=ErrorSchema,
                description="No autorizado",
            )
        }
    )
    def get(self, request, codigo_provincia_or_slug):

        try:
            return JsonResponse([
                {
                    "codigo": municipio.codigo,
                    "nombre": municipio.nombre,
                    "nombre_slug": municipio.nombre_slug,
                    "nombre_alternativo": municipio.nombre_alternativo,
                    "nombre_alternativo_slug": municipio.nombre_alternativo_slug
                }

                # Buscar en el codigo, nombre slug, nombre alternativo slug
                for municipio in Municipio.objects.prefetch_related('provincia').filter(
                    Q(provincia__codigo=codigo_provincia_or_slug) |
                    Q(provincia__nombre_slug=codigo_provincia_or_slug) |
                    Q(provincia__nombre_alternativo_slug=codigo_provincia_or_slug)
                )
            ], safe=False)

        except ComunidadAutonoma.DoesNotExist:
            return JsonResponse({"error": "La comunidad autónoma no existe."})
