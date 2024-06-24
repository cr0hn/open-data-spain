from rest_framework import serializers


class GeoLocationSerializer(serializers.Serializer):
    latitud = serializers.FloatField(help_text="Latitud de la geolocalización", min_value=-90, max_value=90, required=True)
    longitud = serializers.FloatField(help_text="Longitud de la geolocalización", min_value=-180, max_value=180, required=True)
    radio = serializers.IntegerField(help_text="Radio de búsqueda en metros", min_value=0, max_value=20_000, default=5000, required=False)
