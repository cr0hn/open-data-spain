UserMeSchemaResponse = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'username': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'consumed_services': {
            'type': 'object',
            'properties': {
                'geo_politico': {'type': 'integer'},
                'subastas_boe': {'type': 'integer'},
            }
        }
    }
}

UnauthorizedErrorSchema = {
    'type': 'object',
    'properties': {
        'message': {'type': 'string'}
    }
}


__all__ = (
    "UnauthorizedErrorSchema", "UserMeSchemaResponse"
)
