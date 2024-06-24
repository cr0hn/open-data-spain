import datetime

from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.paginator import Paginator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiExample, OpenApiResponse

from sdk.views import get_page, get_page_size
from dashboard.api_keys.authentication import TokenAuthentication
from apps.geopolitico.models import Provincia, ComunidadAutonoma

from ...models import SubastaBOE
from .serializers import GeoLocationSerializer
from .sdk import build_detalle_subasta, build_resumen_subasta, build_bien_detalle
from .openapi import UnauthorizedErrorSchema, ListarSubastasHoySchema, NotFoundSchema, DetalleSubastaSchema, ListarBienesGeoLocationSchema, \
    DetalleBienSchema


class GetSubastasHoy(APIView):
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return SubastaBOE.objects.filter(fecha_creacion__date=datetime.date.today()).order_by('-fecha_creacion')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='Número de página',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            ),
            OpenApiParameter(
                name='page_size',
                location=OpenApiParameter.QUERY,
                description='Tamaño de página. Valores permitidos: 1-25',
                required=False,
                type=OpenApiTypes.INT,
                default=10,
            ),
        ],
        operation_id="Listar Subastas Hoy",
        tags=['subastas-publicas-boe'],
        description="""Devuelve la lista de subastas de hoy para todas las provincias.

Cada entrada de la lista contiene el resumen de la subasta, así como de los lotes totales e inmuebles totales que contiene.

Soporta paginación. Puedes usar los parámetros `page` y `page_size` para cambiar la página y el tamaño de página.
""",
        responses={
            200: OpenApiResponse(
                response=ListarSubastasHoySchema,
                description="Lista de subastas de hoy para todas las provincias",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de respuesta",
                        value={
                            "total": 1,
                            "page": 1,
                            "page_size": 10,
                            "results": [
                                {
                                    "id": 1,
                                    "provincia": "Madrid",
                                    "municipio": "Madrid",
                                    "fecha_creacion": "2021-08-29T12:00:00Z",
                                    "fecha_inicio": "2021-08-29T12:00:00Z",
                                    "fecha_fin": "2021-08-29T12:00:00Z",
                                    "lotes_totales": 1,
                                    "inmuebles_totales": 1
                                }
                            ]
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=UnauthorizedErrorSchema,
                description="No se ha enviado el token de autenticación o el token es inválido",
            )
        }
    )
    def get(self, _request, *args, **kwargs):
        page = get_page(_request)
        page_size = get_page_size(_request, max_allowed=25)

        paginator = Paginator(self.get_queryset(), page_size)
        page_obj = paginator.page(page)

        subasta_results = []
        subasta_append = subasta_results.append

        for subasta in page_obj:
            subasta_append(build_resumen_subasta(subasta))

        ret = {
            'total': paginator.count,
            'page': page_obj.number,
            'page_size': page_size,
            'results': subasta_results
        }

        return JsonResponse(ret, safe=False)


class GetDetalleSubasta(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        operation_id="Detalle Subasta",
        tags=['subastas-publicas-boe'],
        description="Devuelve el detalle de una subasta a partir de su identificador",
        responses={
            200: OpenApiResponse(
                response=DetalleSubastaSchema,
                description="Detalle de la subasta",
            ),
            401: OpenApiResponse(
                response=UnauthorizedErrorSchema,
                description="No se ha enviado el token de autenticación o el token es inválido",
            ),
            404: OpenApiResponse(
                response=NotFoundSchema,
                description="No se encontró la subasta",
            )
        }
    )
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')  # Obtener el valor de 'pk' de los argumentos de la vista

        try:
            instance = SubastaBOE.objects.get(pk=pk)
        except SubastaBOE.DoesNotExist:
            return JsonResponse({'error': 'No se encontró la subasta con la clave primaria (pk) proporcionada.'}, status=404)

        return JsonResponse(build_detalle_subasta(instance))


class GetDetalleBien(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        operation_id="Detalle Bien",
        tags=['subastas-publicas-boe'],
        description="Devuelve el detalle de un bien a partir de su identificador",
        responses={
            200: OpenApiResponse(
                response=DetalleBienSchema,
                description="Detalle del bien",
            ),
            401: OpenApiResponse(
                response=UnauthorizedErrorSchema,
                description="No se ha enviado el token de autenticación o el token es inválido",
            ),
            404: OpenApiResponse(
                response=NotFoundSchema,
                description="No se encontró la subasta",
            )
        }
    )
    def get(self, request, *args, **kwargs):
        ...
    # def get(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')  # Obtener el valor de 'pk' de los argumentos de la vista
    #
    #     try:
    #         instance = BoeBienesDetalle.objects.get(bien_id=pk)
    #
    #         return JsonResponse(build_bien_detalle(instance.extra))
    #
    #     except BoeBienesDetalle.DoesNotExist:
    #         return JsonResponse({'error': 'No se encontró la subasta con la clave primaria (pk) proporcionada.'}, status=404)


class SubastasProvinciaComunidad(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, _request, *args, **kwargs):

        # -------------------------------------------------------------------------
        # Configuración de parámetros para las Provincias y Comunidades Autónomas
        # -------------------------------------------------------------------------
        comunidad = kwargs.get('comunidad')
        provincia = kwargs.get('provincia')

        provincia_obj = None
        comunidad_obj = None

        if provincia is None and comunidad is None:
            return JsonResponse({'error': 'Tienes que proporcionar la comunidad y la provincia'}, status=400)

        # Si no se ha proporcionado el municipio, se buscará por provincia
        elif provincia is None:

            try:
                comunidad_obj = ComunidadAutonoma.objects.get(
                    Q(codigo=comunidad) |
                    Q(nombre__contains=comunidad) |
                    Q(nombre_slug=comunidad)
                )
            except ComunidadAutonoma.DoesNotExist:
                return JsonResponse({'error': 'No se encontró la comunidad autónoma'}, status=404)

        # Si se ha proporcionado el municipio, se buscará por provincia y municipio
        else:
            try:
                provincia_obj = Provincia.objects.prefetch_related('comunidad_autonoma').filter(
                    Q(codigo=provincia) |
                    Q(nombre_slug=provincia) |
                    Q(nombre__contains=provincia) |
                    Q(nombre_alternativo_slug__contains=provincia) &

                    Q(comunidad_autonoma__codigo=comunidad) |
                    Q(comunidad_autonoma__nombre__contains=comunidad) |
                    Q(comunidad_autonoma__nombre_slug=comunidad) |
                    Q(comunidad_autonoma__nombre_alternativo__contains=comunidad) |
                    Q(comunidad_autonoma__nombre_alternativo_slug=comunidad)
                ).first()
            except Provincia.DoesNotExist:
                return JsonResponse({'error': 'No se encontró la provincia'}, status=404)

        if not provincia_obj and not comunidad_obj:
            return JsonResponse({'error': 'No se la provincia o comunidad proporcionada no existe.'}, status=404)

        # -------------------------------------------------------------------------
        # Creando la Query
        # -------------------------------------------------------------------------
        config = {}

        if provincia_obj:
            config['provincia'] = provincia_obj

        if comunidad_obj:
            config['comunidad'] = comunidad_obj

        query_set = SubastaBOE.objects.filter(**config).order_by('-fecha_creacion')

        # -------------------------------------------------------------------------
        # Paginación
        # -------------------------------------------------------------------------
        page = get_page(_request)
        page_size = get_page_size(_request, max_allowed=25)

        paginator = Paginator(query_set, page_size)
        page_obj = paginator.page(page)

        subasta_results = []
        subasta_append = subasta_results.append

        for subasta in page_obj:
            subasta_append(build_resumen_subasta(subasta))

        ret = {
            'total': paginator.count,
            'page': page_obj.number,
            'page_size': page_size,
            'results': subasta_results
        }

        return JsonResponse(ret, safe=False)


class SubastasComunidad(SubastasProvinciaComunidad):

    @extend_schema(
        operation_id="Subastas por Comunidad Autónoma",
        tags=['subastas-publicas-boe'],
        description="Devuelve el lista de subastas en una comunidad autónoma",
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='Número de página',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            ),
            OpenApiParameter(
                name='page_size',
                location=OpenApiParameter.QUERY,
                description='Tamaño de página. Valores permitidos: 1-25',
                required=False,
                type=OpenApiTypes.INT,
                default=10,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=ListarSubastasHoySchema,
                description="Detalle de la subasta",
            ),
            401: OpenApiResponse(
                response=UnauthorizedErrorSchema,
                description="No se ha enviado el token de autenticación o el token es inválido",
            ),
            404: OpenApiResponse(
                response=NotFoundSchema,
                description="No se encontró la subasta",
            )
        }
    )
    def get(self, _request, *args, **kwargs):
        return super().get(_request, *args, **kwargs)


class SubastasComunidadProvincia(SubastasProvinciaComunidad):

    @extend_schema(
        operation_id="Subastas por Comunidad Autónoma y Provincia",
        tags=['subastas-publicas-boe'],
        description="Devuelve el lista de subastas en una comunidad autónoma y provincia",
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='Número de página',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            ),
            OpenApiParameter(
                name='page_size',
                location=OpenApiParameter.QUERY,
                description='Tamaño de página. Valores permitidos: 1-25',
                required=False,
                type=OpenApiTypes.INT,
                default=10,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=ListarSubastasHoySchema,
                description="Detalle de la subasta",
            ),
            401: OpenApiResponse(
                response=UnauthorizedErrorSchema,
                description="No se ha enviado el token de autenticación o el token es inválido",
            ),
            404: OpenApiResponse(
                response=NotFoundSchema,
                description="No se encontró la subasta",
            )
        }
    )
    def get(self, _request, *args, **kwargs):
        return super().get(_request, *args, **kwargs)


class SearchGeoLocation(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        operation_id="Buscar subastas por geolocalización",
        tags=['subastas-publicas-boe'],
        description="Devuelve el lista de subastas en una comunidad autónoma y provincia",
        request=GeoLocationSerializer,
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='Número de página',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            ),
            OpenApiParameter(
                name='page_size',
                location=OpenApiParameter.QUERY,
                description='Tamaño de página. Valores permitidos: 1-25',
                required=False,
                type=OpenApiTypes.INT,
                default=10,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=ListarBienesGeoLocationSchema,
                description="Detalle de la subasta",
            ),
            401: OpenApiResponse(
                response=UnauthorizedErrorSchema,
                description="No se ha enviado el token de autenticación o el token es inválido",
            ),
            404: OpenApiResponse(
                response=NotFoundSchema,
                description="No se encontró la subasta",
            )
        }
    )
    def post(self, _request):
        ...
    # def post(self, _request):
    #
    #     try:
    #         json_data = JSONParser().parse(_request)
    #     except:
    #         return JsonResponse({'error': 'No se ha proporcionado un JSON válido'}, status=400)
    #
    #     serializer = GeoLocationSerializer(data=json_data)
    #
    #     if not serializer.is_valid():
    #         return JsonResponse(serializer.errors, status=400)
    #
    #     data = serializer.validated_data
    #
    #     lat = data.get('latitud')
    #     lon = data.get('longitud')
    #     radio = data.get('radio')
    #
    #     point = Point(lon, lat, srid=4326)
    #
    #     page = get_page(_request)
    #     page_size = get_page_size(_request, max_allowed=25)
    #
    #     # query_set = BienesGeoLocated.objects.prefetch_related('subasta').filter(
    #     #     location__distance_lte=(point, radio)
    #     # ).order_by('location')
    #
    #     # query_set = BienesGeoLocated.objects.prefetch_related('subasta').filter(
    #     #     location__distance_lte=(point, D(km=radio))
    #     # ).extra(
    #     #     select={'distance': 'ST_Distance(location, ST_GeomFromEWKT(%s))'},
    #     #     select_params=(point.ewkt,)
    #     # ).order_by('location')
    #
    #     paginator = Paginator(query_set, page_size)
    #     page_obj = paginator.page(page)
    #
    #     subasta_results = []
    #     subasta_append = subasta_results.append
    #
    #     for bien in page_obj:
    #         subasta_append({
    #             'subasta': bien.subasta.pk,
    #             'bien': bien.pk,
    #             'lat': bien.lat,
    #             'lon': bien.lng,
    #             'distancia': int(bien.distance * 1000),  # en metros
    #         })
    #
    #     ret = {
    #         'total': paginator.count,
    #         'page': page_obj.number,
    #         'page_size': page_size,
    #         'results': subasta_results
    #     }
    #
    #     return JsonResponse(ret, safe=False)
