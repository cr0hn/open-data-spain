import hashlib

from dataclasses import dataclass

import googlemaps

from apps.cache.models import Cache
from sdk.text import text_remove_spaces, text_remove_spaces_in_parenthesis
from apps.geopolitico.models import Provincia, Municipio, ComunidadAutonoma


# from sdk.core import text_remove_spaces, text_remove_spaces_in_parenthesis, get_db_cache, Geography, set_db_cache


@dataclass
class GoogleLocation:
    calle: str = None
    numero: int = None
    codigo_postal: str = None

    municipio: str = None
    provincia: str = None
    comunidad_autonoma: str = None

    codigo_municipio: str = None
    codigo_provincia: str = None
    codigo_comunidad: str = None

    latitud: str = None
    longitud: str = None

    google_place_id: str = None
    google_maps_raw: dict = None
    google_formatted_address: str = None

    def to_dict(self):
        return {
            "calle": self.calle,
            "numero": self.numero,
            "codigo_postal": self.codigo_postal,
            "municipio": self.municipio,
            "provincia": self.provincia,
            "comunidad_autonoma": self.comunidad_autonoma,
            "codigo_municipio": self.codigo_municipio,
            "codigo_provincia": self.codigo_provincia,
            "codigo_comunidad": self.codigo_comunidad,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "google_place_id": self.google_place_id,
            "google_maps_raw": self.google_maps_raw,
            "google_formatted_address": self.google_formatted_address,
        }


def geolocate(address: str, google_maps_apikey: str, debug: bool = False, convert_geo_to_object: bool = False) -> GoogleLocation | None:
    if debug:
        return None

    if not address:
        return None

    # Clean address
    step1 = text_remove_spaces(address)
    step2 = text_remove_spaces_in_parenthesis(step1)
    address_clean = step2.title().strip()

    cache_key = hashlib.sha256(f"google-maps-{address}".encode()).hexdigest()

    if (cache_data := Cache.get_json(cache_key)) is not None:

        if not cache_data:
            return None

        else:
            return GoogleLocation(**cache_data)

    gclient = googlemaps.Client(key=google_maps_apikey, queries_per_minute=10000, queries_per_second=300)

    if found := gclient.geocode(address_clean, language="es", region="es"):

        config = {}

        res = found[0]

        for inf in res["address_components"]:
            value = inf["long_name"]
            _types = inf["types"]

            # Si no queremos convertir a objeto, no hacemos nada
            if "postal_code" in _types:
                config["codigo_postal"] = value

            elif "street_number" in _types:
                config["numero"] = value

            elif "route" in _types:
                config["calle"] = value

            elif "locality" in _types:

                if convert_geo_to_object:
                    if loc := Municipio.search(value):
                        config["municipio"] = loc.nombre
                        config["codigo_municipio"] = loc.codigo

                else:
                    config["municipio"] = value

            elif "administrative_area_level_2" in _types:

                if convert_geo_to_object:
                    # Si tiene nivel 2, es que tiene nivel 1.
                    if prov := Provincia.search(value):
                        config["provincia"] = prov.nombre
                        config["codigo_provincia"] = prov.codigo

                    elif prov := ComunidadAutonoma.search(value):
                        config["provincia"] = prov.nombre
                        config["codigo_provincia"] = prov.codigo

                else:
                    config["provincia"] = value

            elif "administrative_area_level_1" in _types:

                if convert_geo_to_object:
                    if com := ComunidadAutonoma.search(value):
                        config["comunidad_autonoma"] = com.nombre
                        config["codigo_comunidad"] = com.codigo
                    elif com := Provincia.search(value):
                        config["comunidad_autonoma"] = com.nombre
                        config["codigo_comunidad"] = com.codigo

                else:
                    config["comunidad_autonoma"] = value

            elif "country" in _types:
                pass

        config["google_formatted_address"] = res.get("formatted_address", None)
        config["google_place_id"] = res.get("place_id", None)

        config["latitud"] = res["geometry"]["location"]["lat"]
        config["longitud"] = res["geometry"]["location"]["lng"]
        config["google_maps_raw"] = found

        Cache.set(cache_key, config)

        return GoogleLocation(**config)

    else:
        Cache.set(cache_key, None)


__all__ = ("GoogleLocation", "geolocate")
