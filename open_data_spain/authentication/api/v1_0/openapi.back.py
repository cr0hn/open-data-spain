from drf_yasg import openapi


UserMeSchemaResponse = openapi.Response(
    description="Información del usuario",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING),
            "consumed_services": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "geo_politico": openapi.Schema(type=openapi.TYPE_STRING),
                    "subastas_boe": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "organization": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)

UnauthorizedErrorSchema = openapi.Response(
    description="Unauthorized",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )
)

__all__ = (
    "UnauthorizedErrorSchema", "UserMeSchemaResponse"
)
