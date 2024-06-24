import logging

from django.contrib.gis.geos import Point

from sdk.google_maps import geolocate
from apps.subastas_boe.models import SubastaBOE

logger = logging.getLogger("ods")


def add_geo_data(subasta: SubastaBOE):
    found_bienes = []
    bienes_geo = []

    new_extra = dict(subasta.extra).copy()

    for lote_index, lote in enumerate(subasta.extra.get('lotes', [])):
        for bien_index, bien in enumerate(lote.get('bienes', [])):

            d = new_extra['lotes'][lote_index]['bienes'][bien_index]

            # Si ya tiene geo_data, no hacemos nada
            # if "geo_data" in d:
            #     continue

            found_geo_data = False

            if direccion := bien.get('calle'):

                if geo_data := geolocate(direccion, "AIzaSyDy2Xj2pGaDAaO8RvTkJbnpYAWGlMM_SSk"):
                    found_bienes.append({
                        "id": d["id"],
                        'lat': geo_data.latitud,
                        'lng': geo_data.longitud,
                        'location': f'{geo_data.latitud},{geo_data.longitud}',
                        'subasta': subasta.id,
                    })
                    found_geo_data = True

                    d['geo_data'] = {
                        'google_maps': {
                            'google_place_id': geo_data.google_place_id,
                            'formatted_address': geo_data.google_formatted_address,
                        },

                        'geo_json': {
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Point',
                                'coordinates': [geo_data.longitud, geo_data.latitud],
                            },
                            'properties': {
                                'calle': geo_data.calle,
                                'numero': geo_data.numero,
                                'codigo_postal': geo_data.codigo_postal,
                                'municipio': geo_data.municipio,
                                'codigo_municipio': geo_data.codigo_municipio,
                                'provincia': geo_data.provincia,
                                'codigo_provincia': geo_data.codigo_provincia,
                                'comunidad_autonoma': geo_data.comunidad_autonoma,
                                'codigo_comunidad_autonoma': geo_data.codigo_comunidad,
                            },
                        },

                        'lat': geo_data.latitud,
                        'lng': geo_data.longitud,
                    }

                    # Añadimos la información de geolocalización a la tabla BoeBienesDetalle
                    bienes_geo.append({
                        'bien_id': d["id"],
                        'extra': d,
                        'lote_nombre': lote['nombre'],
                    })

            if found_geo_data is False:
                d['geo_data'] = {
                    'google_maps': None,
                    'geo_json': None,
                    'lat': None,
                    'lng': None,
                }

    # Actualizamos la información de los bienes
    subasta.extra = new_extra

    try:
        subasta.save()
    except Exception as e:
        logger.error(f"Error al guardar la información extra de geolocalización de la subasta {subasta.id}: {e}")
        return

    # Si hemos encontrado bienes con geo_data, actualizamos el extra
    if found_bienes:

        # Añadimos la información GeoJSON de cada bien
        for bien in found_bienes:
            try:
                BienesGeoLocated.objects.create(
                    bien_id=bien["id"],
                    lat=bien["lat"],
                    lng=bien["lng"],
                    location=Point(bien["lng"], bien["lat"], srid=4326),
                    subasta_id=bien["subasta"],
                )
            except Exception as e:
                logger.error(f"Error al guardar la información en la tabla BienesGeoLocated del bien {bien['id']}: {e}")

    for bien in bienes_geo:
        try:
            obj = BoeBienesDetalle.objects.get(bien_id=bien["bien_id"])
            obj.extra = bien["extra"]
            obj.save()

        except BoeBienesDetalle.DoesNotExist:

            try:
                BoeBienesDetalle.objects.create(
                    bien_id=bien["bien_id"],
                    extra=bien["extra"],
                    lote_nombre=bien["lote_nombre"],
                    subasta=subasta,
                )
            except Exception as e:
                logger.error(f"Error al guardar la información en la tabla BoeBienesDetalle del bien {bien['id']}: {e}")
