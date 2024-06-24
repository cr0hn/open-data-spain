from apps.subastas_boe.sdk.constants import *


DetalleBienSchema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "cru": {"type": ["string", "null"], 'description': 'Código Registral Único'},
        "calle": {"type": "string"},
        "cargas": {"type": ["boolean", "null"], "description": "Indica si el bien tiene cargas y de qué tipo"},
        "idufir": {"type": ["string", "null"], 'description': 'Identificador Único de Finca Registral'},
        "titulo": {"type": "string"},
        "cabecera": {"type": "string"},
        "geo_data": {
            "type": "object",
            "properties": {
                "lat": {"type": "number", "description": "Latitud"},
                "lng": {"type": "number", "description": "Longitud"},
                "geo_json": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "geometry": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string"},
                                "coordinates": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Longitud y latitud. Formato: [longitud, latitud]"
                                }
                            }
                        },
                        "properties": {
                            "type": "object",
                            "properties": {
                                "calle": {"type": "string"},
                                "numero": {"type": "string"},
                                "municipio": {"type": "string"},
                                "provincia": {"type": "string"},
                                "codigo_postal": {"type": "string"},
                                "codigo_municipio": {"type": "string"},
                                "codigo_provincia": {"type": "string"},
                                "comunidad_autonoma": {"type": "string"},
                                "codigo_comunidad_autonoma": {"type": "string"}
                            }
                        }
                    }
                },
                "google_maps": {
                    "type": "object",
                    "properties": {
                        "google_place_id": {"type": "string", "description": "Google Place ID"},
                        "formatted_address": {"type": "string", "description": "Dirección formateada por Google Maps"},
                    }
                }
            }
        },
        "visitable": {"type": "string", "enum": ["no-consta"], "description": "Indica si el bien es visitable o no"},
        "descripcion": {"type": "string"},
        "cargas_numero": {"type": "integer", "description": "Número de cargas"},
        "codigo_postal": {"type": ["string", "null"]},
        "municipio_slug": {"type": "string"},
        "provincia_slug": {"type": "string"},
        "tipo_propiedad": {"type": "string", "enum": get_values(TipoPropiedad)},
        "titulo_juridico": {"type": ["string", "null"], "description": "Título jurídico del bien"},
        "tipo_construccion": {"type": "string", "enum": get_values(TipoConstruccion)},
        "vivienda_habitual": {"type": ["boolean", "null"], "description": "Indica si el bien es vivienda habitual"},
        "situacion_posesoria": {"type": "string", "enum": get_values(SituacionPosesoria), "description": "Situación posesoria del bien"},
        "referencia_catastral": {"type": ["string", "null"], "description": "Referencia catastral del bien"},
        "informacion_adicional": {"type": ["string", "null"]},
        "inscripcion_registral": {"type": ["string", "null"], "description": "Inscripción registral del bien"},
        "comunidad_autonoma_slug": {"type": "string"},
        "comunidad_autonoma_nombre": {"type": "string"}
    }
}


DetalleSubastaSchema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'boe': {'type': 'string'},
        'url': {'type': 'string'},
        'tipo_fecha': {'type': 'string', 'enum': get_values(TipoFecha)},
        'fecha_inicio': {'type': 'string', 'format': 'date-time', 'nullable': True},
        'fecha_fin': {'type': 'string', 'format': 'date-time', 'nullable': True},
        'fecha_publicacion': {'type': 'string', 'format': 'date-time'},
        'tipo': {'type': 'string', 'enum': get_values(TipoSubasta)},
        'informacion_economica': {
            'type': 'object',
            'properties': {
                'cantidad_reclamada': {'type': 'number'},
                'valor_subasta': {'type': 'number'},
                'tasacion': {'type': 'number'},
                'puja_minima': {'type': 'number'},
                'tramos_pujas': {'type': 'array', 'items': {'type': 'number'}},
                'deposito': {'type': 'number'},
            }
        },
        'localizacion': {
            'type': 'object',
            'properties': {
                'comunidad_autonoma': {'type': 'string'},
                'comunidad_autonoma_slug': {'type': 'string'},
                'provincia': {'type': 'string'},
                'provincia_slug': {'type': 'string'},
            }
        },
        'gestora': {
            'type': 'object',
            'properties': {
                'codigo': {'type': 'string'},
                'descripcion': {'type': 'string'},
                'telefono': {'type': 'string'},
                'fax': {'type': 'string', 'nullable': True},
                'email': {'type': 'string'},
            }
        },
        'acreedor': {
            'type': 'object',
            'properties': {
                'nif': {'type': 'string'},
                'nombre': {'type': 'string'},
                'direccion': {'type': 'string'},
                'codigo_postal': {'type': 'string'},
                'localidad': {'type': 'string'},
                'provincia': {'type': 'string'},
                'tipo_acreedor': {'type': 'string', 'enum': get_values(TipoAcreedor)},
                'banco': {'type': 'string', 'nullable': True, 'enum': get_values(Bancos)},
            }
        },
        'lotes': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'bienes': {
                        'type': 'array',
                        'items': DetalleBienSchema
                    },
                    'id': {'type': 'integer'},
                    'nombre': {'type': 'string'},
                    'descripcion_lote': {'type': 'string'},
                    'tramos_pujas_tipo': {'type': 'string', 'enum': get_values(TramosPujas)},
                    'tramos_pujas': {'type': 'number'},
                    'deposito': {'type': 'number'},
                    'deposito_tipo': {'type': 'string', 'enum': get_values(Deposito)},
                    'informacion_economica': {
                        'type': 'object',
                        'properties': {
                            'total_cantidad_reclamada': {'type': 'number'},
                            'total_valor_subasta': {'type': 'number'},
                            'total_tasacion': {'type': 'number'},
                            'total_deposito': {'type': 'number'},
                        }
                    },
                },
            }
        },
    }
}


ListarSubastasHoySchema = {
    'type': 'object',
    'properties': {
        'total': {'type': 'integer'},
        'page': {'type': 'integer'},
        'page_size': {'type': 'integer'},
        'results': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'boe': {'type': 'string'},
                    'tipo': {'type': 'string', 'enum': get_values(TipoSubasta)},
                    'tipo_fecha': {'type': 'string', 'enum': get_values(TipoFecha)},
                    'fecha_fin': {'type': 'string', 'format': 'date-time'},
                    'fecha_inicio': {'type': 'string', 'format': 'date-time'},
                    'fecha_publicacion': {'type': 'string', 'format': 'date-time'},
                    'informacion_economica': {
                        'type': 'object',
                        'properties': {
                            'total_cantidad_reclamada': {'type': 'number'},
                            'total_valor_subasta': {'type': 'number'},
                            'total_tasacion': {'type': 'number'},
                            'total_deposito': {'type': 'number'}
                        }
                    },
                    'ubicacion': {
                        'type': 'object',
                        'properties': {
                            'comunidad_autonoma': {'type': 'string'},
                            'comunidad_autonoma_slug': {'type': 'string'},
                            'provincia': {'type': 'string'},
                            'provincia_slug': {'type': 'string'},
                        }
                    },
                    'total_lotes': {'type': 'integer'},
                    'total_inmuebles': {'type': 'integer'},
                }
            }
        }
    }
}

ListarBienesGeoLocationSchema = {
    'type': 'object',
    'properties': {
        'total': {'type': 'integer'},
        'page': {'type': 'integer'},
        'page_size': {'type': 'integer'},
        'results': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'subasta': {'type': 'integer', 'description': 'Id de la subasta a la que pertenece el bien'},
                    'bien': {'type': 'integer', 'description': 'Id del bien'},
                    'lat': {'type': 'number', 'description': 'Latitud en la que se encuentra el bien'},
                    'lon': {'type': 'number', 'description': 'Longitud en la que se encuentra el bien'},
                    'distancia': {'type': 'integer', 'description': 'Distancia en metros desde el punto de referencia'},
                }
            }
        }
    }
}


NotFoundSchema = {
    'type': 'object',
    'properties': {
        'error': {'type': 'string'}
    }
}

UnauthorizedErrorSchema = {
    'type': 'object',
    'properties': {
        'message': {'type': 'string'}
    }
}
