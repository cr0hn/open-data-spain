

from __future__ import annotations

import uuid

from mongoengine import Document, fields, EmbeddedDocument, CASCADE

from apps.subastas_boe.sdk import constants
from apps.geopolitico.models import Provincia, Municipio, ComunidadAutonoma


class BienBOE(EmbeddedDocument):
    id = fields.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    cabecera = fields.StringField(blank=True, null=True)
    titulo = fields.StringField(blank=True, null=True)
    descripcion = fields.StringField(blank=True, null=True)

    # Tamaño del inmueble
    tamanio = fields.FloatField(null=True, blank=True, default=None)
    direccion_completa = fields.StringField(blank=True, null=True)

    tipo_construccion = fields.StringField(max_length=25, blank=False, null=False, choices=[
        (constants.TipoConstruccion.CASA, "Casa"),
        (constants.TipoConstruccion.PISO, "Piso"),
        (constants.TipoConstruccion.NAVE, "Nave"),
        (constants.TipoConstruccion.ATICO, "Ático"),
        (constants.TipoConstruccion.LOCAL_COMERCIAL, "Local comercial"),
        (constants.TipoConstruccion.COMERCIO, "Comercio"),
        (constants.TipoConstruccion.GARAGE, "Garage"),
        (constants.TipoConstruccion.FINCA_PARCELA, "Finca / parcela"),
        (constants.TipoConstruccion.TRASTERO, "Trastero"),
        (constants.TipoConstruccion.DUPLEX, "Duplex"),
        (constants.TipoConstruccion.ALMACEN, "Almacén"),
        (constants.TipoConstruccion.SOLAR, "Solar"),
        (constants.TipoConstruccion.OFICINA, "Oficina"),
        (constants.TipoConstruccion.PAJAR, "Pajar"),
        (constants.TipoConstruccion.CUADRA, "Cuadra"),
        (constants.TipoConstruccion.OTHER, "Otro"),
    ], default=constants.TipoConstruccion.OTHER)
    tipo_propiedad = fields.StringField(max_length=25, blank=False, null=False, choices=[
        (constants.TipoPropiedad.URBANO, "Urbano"),
        (constants.TipoPropiedad.RUSTICO, "Rústico"),
        (constants.TipoPropiedad.DESCONOCIDO, "Desconocido"),
    ], default=constants.TipoPropiedad.DESCONOCIDO)

    titulo_juridico = fields.StringField(null=False, blank=False, choices=[
        (constants.TituloJuridico.PLENO_DOMINIO, "pleno dominio"),
        (constants.TituloJuridico.PARTE, "parte"),
        (constants.TituloJuridico.DESCONOCIDO, "desconocido"),
    ], default=constants.TituloJuridico.DESCONOCIDO)

    situacion_posesoria = fields.StringField(null=False, blank=False, choices=[
        (constants.SituacionPosesoria.DERECHO_PERMANENCIA, "derecho de permanencia"),
        (constants.SituacionPosesoria.DERECHO_USO, "derecho de uso"),
        (constants.SituacionPosesoria.OCUPANTE_DESCONOCIDO, "ocupante desconocido"),
        (constants.SituacionPosesoria.SIN_OCUPANTES, "sin ocupantes"),
        (constants.SituacionPosesoria.NO_CONSTA, "no consta"),
        (constants.SituacionPosesoria.DESCONOCIDO, "desconocido"),
        (constants.SituacionPosesoria.PORCENTAJE_50, "50 por ciento"),
    ], default=constants.SituacionPosesoria.DESCONOCIDO)

    visitable = fields.StringField(null=False, blank=False, choices=[
        (constants.Visitable.SI, "si"),
        (constants.Visitable.NO, "no"),
        (constants.Visitable.NO_CONSTA, "no consta")
    ], default=constants.Visitable.NO_CONSTA)

    cargas = fields.StringField(max_length=60, choices=[
        (constants.Cargas.SIN_CARGAS, "Sin cargas"),
        (constants.Cargas.CON_CARGAS, "Con cargas"),
        (constants.Cargas.NO_CONSTA, "No consta"),
        (constants.Cargas.REGISTRADORES, "en registradores.org"),
        (constants.Cargas.DOCUMENTO_EXTERNO, "Documento externo"),
        (constants.Cargas.DESCONOCIDO, "Desconocido"),
    ], default=constants.Cargas.DESCONOCIDO)
    cargas_numero = fields.DecimalField(decimal_places=2, default=0, max_digits=25)

    vivienda_habitual = fields.StringField(max_length=40, null=False, blank=False, choices=[
        (constants.ViviendaHabitual.SI, "Sí"),
        (constants.ViviendaHabitual.NO, "No"),
        (constants.ViviendaHabitual.DESCONOCIDO, "Desconocido"),
    ], default=constants.ViviendaHabitual.DESCONOCIDO)

    informacion_adicional = fields.StringField(null=True, blank=True)

    idufir = fields.StringField(max_length=80, null=True, blank=True)
    cru = fields.StringField(null=True, blank=True)
    inscripcion_registral = fields.StringField(null=True, blank=True)
    referencia_catastral = fields.StringField(null=True, blank=True)

    # -------------------------------------------------------------------------
    # Ubicación
    # -------------------------------------------------------------------------
    codigo_postal = fields.StringField(max_length=6, null=True, blank=True)
    calle = fields.StringField(max_length=250, null=True, blank=True)

    # -------------------------------------------------------------------------
    # Geo-localización
    # -------------------------------------------------------------------------
    lat = fields.PointField(null=True)
    lng = fields.PointField(null=True)

    ubicacion_gps = fields.PointField(srid=4326, help_text='Ubicación GPS', null=True, blank=True)

    google_formatted_address = fields.StringField(null=True, blank=True, unique=True)
    google_place_id = fields.StringField(null=True, blank=True, unique=True)

    # -------------------------------------------------------------------------
    # Relaciones
    # -------------------------------------------------------------------------
    # municipio = fields.ReferenceField(Municipio, null=True, blank=True, reverse_delete_rule=CASCADE)
    # provincia = fields.ReferenceField(Provincia, null=True, blank=True, reverse_delete_rule=CASCADE)
    # comunidad_autonoma = fields.ReferenceField(ComunidadAutonoma, null=True, blank=True, reverse_delete_rule=CASCADE)


class AcreedorBOE(EmbeddedDocument):
    id = fields.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    nif = fields.StringField(max_length=50, unique=True)
    pais = fields.StringField(max_length=50, default="España")
    nombre = fields.StringField(max_length=200, null=True, blank=True)
    tipo_acreedor = fields.StringField(max_length=200, null=False, blank=False, choices=[
        (constants.TipoAcreedor.BANCO, "Banco"),
        (constants.TipoAcreedor.EMPRESA, "Empresa"),
        (constants.TipoAcreedor.OTRO, "Otro"),
        (constants.TipoAcreedor.DESCONOCIDO, "Desconocido"),
        (constants.TipoAcreedor.PARTICULAR, "Particular"),
    ], default=constants.TipoAcreedor.DESCONOCIDO)

    direccion = fields.StringField(max_length=400, null=True, blank=True)
    codigo_postal = fields.StringField(max_length=200, null=True, blank=True)

    # -------------------------------------------------------------------------
    # Relaciones
    # -------------------------------------------------------------------------
    # municipio = fields.ReferenceField(Municipio, null=True, blank=True, reverse_delete_rule=CASCADE)
    # provincia = fields.ReferenceField(Provincia, null=True, blank=True, reverse_delete_rule=CASCADE)


class GestoraBOE(EmbeddedDocument):
    id = fields.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    codigo = fields.StringField(max_length=250, null=False, blank=False)
    descripcion = fields.StringField(max_length=200, null=True, blank=True)
    fax = fields.StringField(max_length=200, null=True, blank=True)
    email = fields.EmailField(max_length=200, null=True, blank=True)
    telefono = fields.StringField(max_length=200, null=True, blank=True)
    direccion = fields.StringField(max_length=200, null=True, blank=True)


class LoteBOE(EmbeddedDocument):
    """
    Ejemplo con varios lotes:

    - https://subastas.boe.es/detalleSubasta.php?idSub=SUB-JA-2021-179138&ver=1&

    """
    id = fields.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    nombre = fields.StringField(max_length=255, null=True, blank=True)
    descripcion = fields.StringField(null=True, blank=True)

    # -------------------------------------------------------------------------
    # Información de subasta
    # -------------------------------------------------------------------------
    cantidad_reclamada = fields.DecimalField(decimal_places=2, default=0, max_digits=25)

    valor_subasta = fields.DecimalField(decimal_places=2, default=0, max_digits=25)
    valor_subasta_tipo = fields.StringField(max_length=30, null=False, blank=False, choices=[
        (constants.ValorSubasta.POR_LOTE, "Por lote"),
        (constants.ValorSubasta.GENERAL, "General"),
        (constants.ValorSubasta.DESCONOCIDO, "Desconocido"),
    ], default=constants.ValorSubasta.DESCONOCIDO)

    tasacion = fields.DecimalField(decimal_places=2, default=0, max_digits=25)
    tasacion_tipo = fields.StringField(max_length=30, null=False, blank=False, choices=[
        (constants.Tasacion.CON_TASACION, "Con tasación"),
        (constants.Tasacion.SIN_TASACION, "Sin tasación"),
        (constants.Tasacion.POR_LOTE, "Por lote"),
        (constants.Tasacion.NO_CONSTA, "Sin tasación"),
        (constants.Tasacion.DESCONOCIDO, "Desconocido"),
    ], default=constants.Tasacion.DESCONOCIDO)

    deposito = fields.DecimalField(decimal_places=2, default=0, max_digits=25)
    deposito_tipo = fields.StringField(max_length=30, null=False, blank=False, choices=[
        (constants.Deposito.NECESARIO, "Necesario"),
        (constants.Deposito.NO_NECESARIO, "No necesario"),
        (constants.Deposito.NO_CONSTA, "No consta"),
        (constants.Deposito.POR_LOTE, "Por lote"),
        (constants.Deposito.DESCONOCIDO, "Desconocido")
    ], default=constants.Deposito.DESCONOCIDO)

    puja_minima = fields.DecimalField(decimal_places=2, default=0, max_digits=25)
    puja_minima_tipo = fields.StringField(max_length=30, null=False, blank=False, choices=[
        (constants.PujaMinima.SIN_PUJA_MINIMA, "Sin puja mínima"),
        (constants.PujaMinima.CON_PUJA_MINIMA, "Con puja mínima"),
        (constants.PujaMinima.POR_LOTE, "Por lote"),
        (constants.PujaMinima.NO_CONSTA, "No consta"),
        (constants.PujaMinima.DESCONOCIDO, "Desconocido"),
    ], default=constants.PujaMinima.DESCONOCIDO)

    tramos_pujas = fields.DecimalField(decimal_places=2, default=0, max_digits=25)
    tramos_pujas_tipo = fields.StringField(max_length=30, null=False, blank=False, choices=[
        (constants.TramosPujas.CON_TRAMOS, "Con tramos"),
        (constants.TramosPujas.SIN_TRAMOS, "Sin tramos"),
        (constants.TramosPujas.NO_CONSTA, "No consta"),
        (constants.TramosPujas.POR_LOTE, "Por lote"),
        (constants.TramosPujas.DESCONOCIDO, "Desconocido")
    ], default=constants.TramosPujas.DESCONOCIDO)

    bienes = fields.EmbeddedDocumentListField(BienBOE)


class SubastaBOE(Document):
    identificador = fields.StringField(primary_key=True)
    url = fields.URLField(max_length=1200)

    fecha_fin = fields.DateTimeField(null=True)
    fecha_inicio = fields.DateTimeField(null=True)
    fecha_creacion = fields.DateTimeField(auto_now=True)

    tipo_subasta = fields.StringField(null=False, blank=False, choices=[
        (constants.TipoSubasta.SEGURIDAD_SOCIAL, "Seguridad Social"),
        (constants.TipoSubasta.HACIENDA, "Hacienda"),
        (constants.TipoSubasta.NOTARIAL, "Notarial"),
        (constants.TipoSubasta.JUDICIAL, "Judicial"),
        (constants.TipoSubasta.DESCONOCIDO, "Desconocido")
    ], default=constants.TipoSubasta.DESCONOCIDO)

    lotes = fields.EmbeddedDocumentListField(LoteBOE)
    gestora = fields.EmbeddedDocumentField(GestoraBOE, null=True, blank=True)

    # comunidad = fields.ReferenceField(ComunidadAutonoma, null=True, blank=True, reverse_delete_rule=CASCADE)
    # provincia = fields.ReferenceField(Provincia, null=True, blank=True, reverse_delete_rule=CASCADE)

    meta = {
        "collection": "boe-subasta",
        "indexes": [
            "fecha_fin",
            "fecha_inicio",
            "fecha_creacion",
            "tipo_subasta",
        ]
    }
