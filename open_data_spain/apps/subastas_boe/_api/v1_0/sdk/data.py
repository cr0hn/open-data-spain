from apps.subastas_boe.models import SubastaBOE


def build_bien_detalle(bien: dict) -> dict:
    return {
        k: v
        for k, v in bien.items()
        if k in (
            'id', 'cabecera', 'titulo', 'descripcion', 'tipo_construccion', 'tipo_propiedad',
            'titulo_juridico', 'situacion_posesoria', 'visitable', 'cargas', 'cargas_numero',
            'vivienda_habitual', 'idufir', 'cru', 'inscripcion_registral', 'referencia_catastral',
            'codigo_postal', 'calle', 'informacion_adicional',

            'provincia_slug', 'provincia_nombre',
            'municipio_slug', 'municipio_nombre',
            'comunidad_autonoma_slug', 'comunidad_autonoma_nombre',
            'geo_data'
        )
    }


def build_detalle_subasta(subasta: SubastaBOE) -> dict:
    data: dict = subasta.extra

    # Acreedora
    if acreedora := data.get('acreedora'):
        acreedora = {
            'nif': acreedora['nif'],
            'nombre': acreedora['nombre'],
            'direccion': acreedora['direccion'],
            'codigo_postal': acreedora['codigo_postal'],
            'localidad': acreedora['localidad'],
            'provincia': acreedora['provincia'],
            'tipo_acreedor': acreedora['tipo_acreedor'],
            'banco': acreedora['banco']

        }
    else:
        acreedora = None

    # Lotes
    lotes = []
    lotes_append = lotes.append

    for lote in data.get('lotes', []):

        bienes = []
        bienes_append = bienes.append

        for bien in lote.get('bienes', []):
            bienes_append(build_bien_detalle(bien))

        # Información económica del lote
        if ie := lote.get('informacion_economica'):
            economic = {
                k: v
                for k, v in ie.items()
                if k in (
                    'cantidad_reclamada', 'valor_subasta', 'tasacion', 'puja_minima', 'tramos_pujas', 'deposito'
                )
            }
        else:
            economic = None

        lotes_append({
            'bienes': bienes,

            # Lote Metadata
            'id': lote['id'],
            'nombre': lote['nombre'],
            'descripcion_lote': lote['descripcion_lote'],

            'informacion_economica': economic
        })

        return {
            'id': subasta.id,
            'boe': subasta.identificador,
            'url': subasta.url,
            'tipo_fecha': data['tipo_fecha'],
            'fecha_inicio': subasta.fecha_fin,
            'fecha_fin': subasta.fecha_inicio,
            'fecha_publicacion': subasta.fecha_creacion,

            'tipo': subasta.tipo_subasta,

            # Economic
            'informacion_economica': {
                'cantidad_reclamada': data['cantidad_reclamada'],
                'valor_subasta': data['total_valor_subasta'],
                'tasacion': data['total_tasacion'],
                'puja_minima': data['total_puja_minima'],
                'tramos_pujas': data['tramos_pujas'],
                'deposito': data['total_deposito']
            },

            # Location
            'localizacion': {
                'comunidad_autonoma': subasta.comunidad.nombre,
                'comunidad_autonoma_slug': subasta.comunidad.nombre_slug,
                'provincia': subasta.provincia.nombre,
                'provincia_slug': subasta.provincia.nombre_slug,
            },

            # Gestora
            'gestora': {
                'codigo': data['gestora']['codigo'],
                'descripcion': data['gestora']['descripcion'],
                'telefono': data['gestora']['telefono'],
                'fax': data['gestora']['fax'],
                'email': data['gestora']['email'],
            },

            # Acreedora
            'acreedor': acreedora,

            # Lotes
            'lotes': lotes,
        }


def build_resumen_subasta(subasta: SubastaBOE) -> dict:
    data: dict = subasta.extra

    total_lotes = len(data.get('lotes', []))
    total_inmuebles = sum([len(lote.get('bienes', [])) for lote in data.get('lotes', [])])

    return {
        'id': subasta.id,
        'boe': subasta.identificador,
        'tipo': subasta.tipo_subasta,

        'tipo_fecha': data['tipo_fecha'],
        'fecha_fin': subasta.fecha_inicio,
        'fecha_inicio': subasta.fecha_fin,
        'fecha_publicacion': subasta.fecha_creacion,

        # Economic
        'informacion_economica': {
            'total_cantidad_reclamada': data['cantidad_reclamada'],
            'total_valor_subasta': data['total_valor_subasta'],
            'total_tasacion': data['total_tasacion'],
            'total_deposito': data['total_deposito']
        },

        # Location
        'ubicacion': {
            'comunidad_autonoma': subasta.comunidad.nombre,
            'comunidad_autonoma_slug': subasta.comunidad.nombre_slug,
            'provincia': subasta.provincia.nombre,
            'provincia_slug': subasta.provincia.nombre_slug,
        },

        'total_lotes': total_lotes,
        'total_inmuebles': total_inmuebles,
    }


__all__ = ('build_detalle_subasta', 'build_resumen_subasta', 'build_bien_detalle')
