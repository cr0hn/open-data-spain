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


def build_detalle_subasta(subasta: dict) -> dict:

    # Acreedora
    if acreedora := subasta.get('acreedora'):

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

    for lote in subasta.get('lotes', []):

        bienes = []
        bienes_append = bienes.append

        for bien in lote.get('bienes', []):
            bienes_append(build_bien_detalle(bien))

        # Información económica del lote
        if ie := lote.get('informacionEconomica'):
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
            'descripcionLote': lote['descripcion_lote'],

            'informacionEconomica': economic
        })

        return {
            # 'id': subasta['_id'],
            'boe': subasta['identificador'],
            'url': subasta['url'],
            'tipoFecha': subasta['tipo_fecha'],
            'fechaInicio': subasta['fecha_inicio'],
            'fechaFin': subasta['fecha_fin'],
            'fechaPublicacion': subasta['fecha_creacion'],

            'tipo': subasta['tipo_subasta'],

            # Economic
            'informacionEconomica': {
                'cantidadReclamada': subasta['cantidad_reclamada'],
                'valorSubasta': subasta['total_valor_subasta'],
                'tasacion': subasta['total_tasacion'],
                'pujaMinima': subasta['total_puja_minima'],
                'pujaMinima_tipo': subasta['puja_minima_tipo'],
                'tramosPujas': subasta['tramos_pujas'],
                'tramosPujas_tipo': subasta['tramos_pujas_tipo'],
                'deposito': subasta['total_deposito']
            },

            # Location
            'localizacion': {
                'comunidadAutonoma': subasta.get("comunidad_autonoma"),
                'comunidadAutonoma_slug': subasta.get("comunidad_autonoma_slug"),
                'provincia': subasta.get("provincia"),
                'provinciaSlug': subasta.get("provincia_slug"),
            },

            # Gestora
            'gestora': {
                'codigo': subasta['gestora']['codigo'],
                'descripcion': subasta['gestora']['descripcion'],
                'telefono': subasta['gestora']['telefono'],
                'fax': subasta['gestora']['fax'],
                'email': subasta['gestora']['email'],
            },

            # Acreedora
            'acreedor': acreedora,

            # Lotes
            'lotes': lotes,
        }


def build_resumen_subasta(subasta: dict) -> dict:

    total_lotes = len(subasta.get('lotes', []))
    total_inmuebles = sum([len(lote.get('bienes', [])) for lote in subasta.get('lotes', [])])

    return {
        # 'id': str(subasta['_id']),
        'boe': subasta['identificador'],
        'tipo': subasta['tipo_subasta'],

        'tipoFecha': subasta['tipo_fecha'],
        'fechaFin': subasta['fecha_fin'],
        'fechaInicio': subasta['fecha_inicio'],
        'fechaPublicacion': subasta['fecha_creacion'],

        # Economic
        'informacionEconomica': {
            'totalCantidadReclamada': subasta['cantidad_reclamada'],
            'totalValorSubasta': subasta['total_valor_subasta'],
            'totalTasacion': subasta['total_tasacion'],
            'totalDeposito': subasta['total_deposito']
        },

        # Location
        'ubicacion': {
            'comunidad_autonoma': subasta.get('comunidad_autonoma'),
            'comunidad_autonoma_slug': subasta.get('comunidad_autonoma_slug'),
            'provincia': subasta.get('provincia'),
            'provincia_slug': subasta.get('provincia_slug'),
        },

        'totalLotes': total_lotes,
        'totalInmuebles': total_inmuebles,
    }


__all__ = ('build_detalle_subasta', 'build_resumen_subasta', 'build_bien_detalle')
