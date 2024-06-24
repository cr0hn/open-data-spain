import logging

from django.conf import settings
from django.db import IntegrityError

from geopolitico.sdk.google import geolocate
from subastas_boe.models import GoogleMapsEntry

from geopolitico.models import Municipio, Provincia, ComunidadAutonoma

logger = logging.getLogger("ods")


def add_google_maps(bien: Bien) -> GoogleMapsEntry | None:

    def _make_address(bien: Bien) -> str:
        calle = bien.calle or ""
        municipio = f", {bien.municipio.nombre}" or ""
        provincia = f", {bien.provincia.nombre}" or ""
        comunidad_autonoma = f", {bien.comunidad_autonoma.nombre}" or ""

        if not calle:
            return ""

        else:
            return f"{calle}{municipio}{provincia}{comunidad_autonoma}"

    if not bien.google_maps:
        address = _make_address(bien)

        google_cloud_secret = settings.GOOGLE_CLOUD_SECRET

        if google_location := geolocate(address, google_cloud_secret):

            try:
                provincia = Provincia.objects.get(codigo=google_location.codigo_provincia)
            except Provincia.DoesNotExist:
                provincia = None

            try:
                municipio = Municipio.objects.get(codigo=google_location.codigo_municipio, provincia=provincia)
            except Municipio.DoesNotExist:
                municipio = None

            try:
                comunidad_autonoma = ComunidadAutonoma.objects.get(codigo=google_location.codigo_comunidad)
            except ComunidadAutonoma.DoesNotExist:
                comunidad_autonoma = None

            try:
                google_maps_entry = GoogleMapsEntry.objects.create(
                    calle=google_location.calle,

                    lat=google_location.latitud,
                    lng=google_location.longitud,

                    #ubicacion_gps=f"POINT({google_location.longitud} {google_location.latitud})",

                    google_place_id=google_location.google_place_id,
                    google_formatted_address=google_location.google_formatted_address,
                    google_maps_raw=google_location.google_maps_raw,

                    municipio=municipio,
                    provincia=provincia,
                    comunidad_autonoma=comunidad_autonoma,
                )
            except IntegrityError:
                try:
                    google_maps_entry = GoogleMapsEntry.objects.get(google_formatted_address=google_location.google_formatted_address)
                except GoogleMapsEntry.DoesNotExist:
                    google_maps_entry = None

            if google_maps_entry:
                bien.direccion_completa = google_maps_entry.google_formatted_address
                bien.google_maps = google_maps_entry
                bien.save()

            return google_maps_entry

    else:
        return bien.google_maps


