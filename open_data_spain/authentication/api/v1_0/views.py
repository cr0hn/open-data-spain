from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from dashboard.api_keys.authentication import TokenAuthentication
from apps.tracking.sdk import build_user_cache_key_prefix, Services

from .openapi import *


class UserMe(APIView):
    """Devuelve la información del usuario autenticado."""

    authentication_classes = [TokenAuthentication]

    @extend_schema(
        operation_id="Información del usuario",
        tags=['users'],
        description="""Obtiene la información del usuario autenticado, así como los servicios consumidos por el mismo.

- **id**: Identificador del usuario.
- **username**: Nombre de usuario.
- **email**: Correo electrónico.
- **first_name**: Nombre.
- **last_name**: Apellidos.
- **consumed_services**: Servicios consumidos por el usuario.
    """,
        responses={
            200: OpenApiResponse(
                response=UserMeSchemaResponse,
                description='Información del usuario',
            ),
            401: OpenApiResponse(
                response=UnauthorizedErrorSchema,
                description='No autorizado',
            )
        }
    )
    def get(self, request):
        user = request.user

        redis_connection = settings.REDIS_CONNECTION

        try:
            geo = int(redis_connection.get(build_user_cache_key_prefix(request, Services.GEO_POLITICO)) or 0)
        except (KeyError, TypeError):
            geo = 0

        try:
            subastas = int(redis_connection.get(build_user_cache_key_prefix(request, Services.SUBASTAS_BOE)) or 0)
        except (KeyError, TypeError):
            subastas = 0

        # Get consumed services
        consumed_services = {
            Services.GEO_POLITICO: geo,
            Services.SUBASTAS_BOE: subastas
        }

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "consumed_services": consumed_services
        })


