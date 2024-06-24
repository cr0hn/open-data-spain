import os
import csv

from typing import Dict, List
from collections import defaultdict

from django.core.management.base import BaseCommand

from apps.geopolitico.models import *

HERE = os.path.dirname(os.path.abspath(__file__))


def load_municipios() -> Dict[str, Dict[str, List[str]]]:
    file_path = os.path.abspath(os.path.join(HERE, "geo_political_data/municipios.with.synonyms.csv"))

    ret = defaultdict(lambda: defaultdict(list))

    with open(file_path, newline='', encoding="utf-8") as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

        for row in spam_reader:
            comunidad, provincia, municipio, name = row

            ret[provincia][municipio].append(name)

    return ret


def load_provincias() -> Dict[str, Dict[str, List[str]]]:
    """
    Formato de retorno:

    {
        "codigo comunidad": [(codigo_provincia, nombre), (codigo_provincia, nombre), (codigo_provincia, nombre)],
    }
    """

    file_path = os.path.abspath(os.path.join(HERE, "geo_political_data/provincias_and_comunidades.with.synonyms.csv"))

    ret = defaultdict(lambda: defaultdict(list))

    with open(file_path, newline='', encoding="utf-8") as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

        for row in spam_reader:
            comunidad, provincia, name = row

            ret[comunidad][provincia].append(name)

    return ret


def load_comunidades() -> Dict[str, List[str]]:
    ret = defaultdict(list)

    comunidades_csv_path = os.path.abspath(os.path.join(HERE, "geo_political_data/comunidades.with.synonyms.csv"))

    with open(comunidades_csv_path, newline='', encoding="utf-8") as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in spam_reader:
            comunidad, name = row

            ret[comunidad].append(name)

    return ret


class Command(BaseCommand):
    help = 'Carga los modelos de geo-politicos para España a partir de los datos'

    def create_comunidades(self) -> dict:

        map_comunidades = {}

        # Crear comunidades
        self.stdout.write(self.style.SUCCESS('Creando comunidades...'), ending='')
        for comunidad_code, titles in load_comunidades().items():

            nombre = titles[0]

            if len(titles) > 1:
                nombre_alternativo = titles[1]
            else:
                nombre_alternativo = None

            dm, created = ComunidadAutonoma.objects.get_or_create(
                codigo=comunidad_code,
                nombre=nombre,
                nombre_alternativo=nombre_alternativo
            )

            map_comunidades[comunidad_code] = dm

        self.stdout.write(self.style.SUCCESS('OK!'))

        return map_comunidades

    def create_provincias(self, comunidades: Dict[str, ComunidadAutonoma]) -> dict:

        map_provincias = {}

        self.stdout.write(self.style.SUCCESS('Creando provincias...'), ending='')
        for cod_comunidad, provincias in load_provincias().items():

            for cod_provincia, nombres in provincias.items():
                nombre = nombres[0]

                if len(nombres) > 1:
                    nombre_alternativo = nombres[1]
                else:
                    nombre_alternativo = None

                dm, created = Provincia.objects.get_or_create(
                    codigo=cod_provincia,
                    nombre=nombre,
                    nombre_alternativo=nombre_alternativo,
                    comunidad_autonoma_id=comunidades[cod_comunidad].pk
                )

                map_provincias[cod_provincia] = dm

        self.stdout.write(self.style.SUCCESS('OK!'))
        return map_provincias

    def create_municipios(self, provincias: Dict[str, Provincia]):

        self.stdout.write(self.style.SUCCESS('Creando municipios...'), ending='')
        for cod_comunidad, municipios in load_municipios().items():

            for cod_municipio, nombres in municipios.items():
                nombre = nombres[0]

                if len(nombres) > 1:
                    nombre_alternativo = nombres[1]
                else:
                    if split_name := nombre.split('/', maxsplit=2):

                        if len(split_name) > 1:
                            nombre = split_name[0].strip()
                            nombre_alternativo = split_name[1].strip()

                        else:
                            nombre_alternativo = None

                    else:
                        nombre_alternativo = None

                Municipio.objects.get_or_create(
                    codigo=cod_municipio,
                    nombre=nombre,
                    nombre_alternativo=nombre_alternativo,
                    provincia_id=provincias[cod_comunidad].pk
                )

        self.stdout.write(self.style.SUCCESS('OK!'))

    def handle(self, *args, **options):
        cm = self.create_comunidades()
        pm = self.create_provincias(cm)
        self.create_municipios(pm)
