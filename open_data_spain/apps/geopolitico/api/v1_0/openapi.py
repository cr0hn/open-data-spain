ListAutonomousCommunitiesSchema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'codigo': {'type': 'string'},
            'nombre': {'type': 'string'},
            'nombre_slug': {'type': 'string'},
            'nombre_alternativo': {'type': 'string'},
            'nombre_alternativo_slug': {'type': 'string', 'nullable': True},
        }
    }
}

ListProvincesSchema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'codigo': {'type': 'string'},
            'nombre': {'type': 'string'},
            'nombre_slug': {'type': 'string'},
            'nombre_alternativo': {'type': 'string'},
            'nombre_alternativo_slug': {'type': 'string', 'nullable': True},
        }
    }
}

ListMunicipalitiesSchema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'codigo': {'type': 'string'},
            'nombre': {'type': 'string'},
            'nombre_slug': {'type': 'string'},
            'nombre_alternativo': {'type': 'string'},
            'nombre_alternativo_slug': {'type': 'string', 'nullable': True},
        }
    }
}


ErrorSchema = {
    'type': 'object',
    'properties': {
        'error': {'type': 'string'},
    }
}

__all__ = (
    "ErrorSchema", "ListAutonomousCommunitiesSchema", "ListProvincesSchema", "ListMunicipalitiesSchema"
)
