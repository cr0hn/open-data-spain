import unidecode

from django.db import models
from django.utils.text import slugify
from django.db.models.functions import Length
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector, SearchQuery, SearchRank

from unidecode import unidecode
from model_utils.models import UUIDModel


def full_text_search(model, _query: str):
    search_query = None

    for q in _query.split(" "):
        if q.isdigit():
            continue

        if "/" in q:
            q_split = q.split("/")
            subquery = SearchQuery(q_split[0], search_type='phrase') | SearchQuery(q_split[1], search_type='phrase')

        else:
            subquery = SearchQuery(q, search_type='phrase')

        if search_query is None:
            search_query = subquery
        else:
            search_query &= subquery

    # search_query = SearchQuery(_query)
    search_vector = SearchVector('nombre', 'nombre_alternativo')

    res = model.objects.annotate(
        rank=SearchRank(search_vector, search_query),
        nombre_length=Length('nombre'),
        nombre_alternativo_length=Length('nombre_alternativo')
    ).order_by('-rank', 'nombre_length', 'nombre_alternativo_length').first()

    return res


class ComunidadAutonoma(UUIDModel, models.Model):
    codigo = models.CharField(max_length=2)
    nombre = models.CharField(max_length=150)
    nombre_alternativo = models.CharField(max_length=150, blank=True, null=True)

    nombre_slug = models.CharField(max_length=150, blank=True, null=True)
    nombre_alternativo_slug = models.CharField(max_length=150, blank=True, null=True)

    search_vector = SearchVectorField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre)
        self.nombre_slug = slugify(self.nombre)

        if self.nombre_alternativo:
            self.nombre_alternativo = unidecode(self.nombre_alternativo)
            self.nombre_alternativo_slug = slugify(self.nombre_alternativo)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Comunidad Autónoma"
        verbose_name_plural = "Comunidades Autónomas"
        db_table = "comunidades_autonomas"
        indexes = [
            models.Index(fields=["codigo"]),
            models.Index(fields=["nombre"]),
            models.Index(fields=["nombre_alternativo"]),
            models.Index(fields=["nombre_slug"]),
            models.Index(fields=["nombre_alternativo_slug"]),
            models.Index(fields=["nombre", "nombre_alternativo"]),
            GinIndex(fields=["search_vector"])
        ]

    @classmethod
    def search(cls, _query) -> "ComunidadAutonoma":
        return full_text_search(cls, _query)

    @classmethod
    def from_provincia(cls, provincia):
        return cls.objects.get(id=provincia.comunidad_autonoma_id)


class Provincia(UUIDModel, models.Model):
    codigo = models.CharField(max_length=2)
    nombre = models.CharField(max_length=150)
    nombre_alternativo = models.CharField(max_length=150, blank=True, null=True)

    nombre_slug = models.CharField(max_length=150, blank=True, null=True)
    nombre_alternativo_slug = models.CharField(max_length=150, blank=True, null=True)

    search_vector = SearchVectorField(null=True, blank=True)

    comunidad_autonoma = models.ForeignKey(ComunidadAutonoma, on_delete=models.CASCADE, related_name="provincias")

    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nombre = unidecode(self.nombre)
        self.nombre_slug = slugify(self.nombre)

        if self.nombre_alternativo:
            self.nombre_alternativo = unidecode(self.nombre_alternativo)
            self.nombre_alternativo_slug = slugify(self.nombre_alternativo)

        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        db_table = "provincias"
        indexes = [
            models.Index(fields=["codigo"]),
            models.Index(fields=["nombre"]),
            models.Index(fields=["nombre_alternativo"]),
            models.Index(fields=["nombre_slug"]),
            models.Index(fields=["nombre_alternativo_slug"]),
            models.Index(fields=["nombre", "nombre_alternativo"]),
            GinIndex(fields=["search_vector"])
        ]

    @classmethod
    def search(cls, _query) -> "Provincia":
        return full_text_search(cls, _query)


class Municipio(UUIDModel, models.Model):
    codigo = models.CharField(max_length=5)
    nombre = models.CharField(max_length=150)
    nombre_alternativo = models.CharField(max_length=150, blank=True, null=True)

    nombre_slug = models.CharField(max_length=150, blank=True, null=True)
    nombre_alternativo_slug = models.CharField(max_length=150, blank=True, null=True)

    search_vector = SearchVectorField(null=True, blank=True)

    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name="municipios")

    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nombre = unidecode(self.nombre)
        self.nombre_slug = slugify(self.nombre)

        if self.nombre_alternativo:
            self.nombre_alternativo = unidecode(self.nombre_alternativo)
            self.nombre_alternativo_slug = slugify(self.nombre_alternativo)

        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        db_table = "municipios"
        indexes = [
            models.Index(fields=["nombre"]),
            models.Index(fields=["codigo"]),
            models.Index(fields=["nombre_alternativo"]),
            models.Index(fields=["nombre_slug"]),
            models.Index(fields=["nombre_alternativo_slug"]),
            models.Index(fields=["nombre", "nombre_alternativo"]),
            GinIndex(fields=["search_vector"])
        ]

    @classmethod
    def search(cls, _query) -> "Municipio":
        return full_text_search(cls, _query)
