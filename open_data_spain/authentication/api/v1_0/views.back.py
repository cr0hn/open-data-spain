from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from dashboard.api_keys.authentication import TokenAuthentication
from tracking.sdk import build_user_cache_key_prefix, Services

from .openapi import *


class UserMe(APIView):
    """Devuelve la información del usuario autenticado."""

    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        operation_id="User Me",
        tags=['users'],
        operation_description="""
Obtiene la información del usuario autenticado, así como los servicios consumidos por el mismo.

- **id**: Identificador del usuario.
- **username**: Nombre de usuario.
- **email**: Correo electrónico.
- **first_name**: Nombre.
- **last_name**: Apellidos.
- **consumed_services**: Servicios consumidos por el usuario.
- **organization**: Organización a la que pertenece el usuario.
""",
        responses={
            200: UserMeSchemaResponse,
            401: UnauthorizedErrorSchema
        },
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
            "consumed_services": consumed_services,
            "organization": user.organization,
        })


