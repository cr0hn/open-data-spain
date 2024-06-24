from dataclasses import dataclass

import googlemaps

from cache.models import Cache
from geopolitico.models import Municipio, Provincia, ComunidadAutonoma
from sdk.text import text_remove_spaces, text_remove_spaces_in_parenthesis


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


def geolocate(address: str, google_maps_apikey: str, debug: bool = False) -> GoogleLocation | None:
    if debug:
        return None

    if not address:
        return None

    # Clean address
    step1 = text_remove_spaces(address)
    step2 = text_remove_spaces_in_parenthesis(step1)
    address_clean = step2.title().strip()

    cache_key = f"google-maps-{address}"

    if cache_data := Cache.get_json(cache_key):
        return GoogleLocation(**cache_data)

    gclient = googlemaps.Client(key=google_maps_apikey)

    if found := gclient.geocode(address_clean, language="es", region="es"):

        config = {}

        res = found[0]

        for inf in res["address_components"]:
            value = inf["long_name"]
            _types = inf["types"]

            if "postal_code" in _types:
                config["codigo_postal"] = value

            elif "street_number" in _types:
                config["numero"] = value

            elif "route" in _types:
                config["calle"] = value

            elif "locality" in _types:
                if loc := Municipio.search(value):
                    config["municipio"] = loc.name
                    config["codigo_municipio"] = loc.cod_municipio

            elif "administrative_area_level_2" in _types:
                # Si tiene nivel 2, es que tiene nivel 1.
                if prov := Provincia.search(value):
                    config["provincia"] = prov.name
                    config["codigo_provincia"] = prov.code
                elif prov := ComunidadAutonoma.search(value):
                    config["provincia"] = prov.name
                    config["codigo_provincia"] = prov.cod

            elif "administrative_area_level_1" in _types:

                if com := ComunidadAutonoma.search(value):
                    config["comunidad_autonoma"] = com.name
                    config["codigo_comunidad"] = com.code
                elif com := Provincia.search(value):
                    config["comunidad_autonoma"] = com.name
                    config["codigo_comunidad"] = com.code

            elif "country" in _types:
                pass

        config["google_formatted_address"] = res.get("formatted_address", None)
        config["google_place_id"] = res.get("place_id", None)

        config["latitud"] = res["geometry"]["location"]["lat"]
        config["longitud"] = res["geometry"]["location"]["lng"]
        config["google_maps_raw"] = found

        Cache.set(cache_key, config)

        return GoogleLocation(**config)


__all__ = ("GoogleLocation", "geolocate")
