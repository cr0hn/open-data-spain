import os
import csv

from typing import Dict
from collections import defaultdict

from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.support.charset import accent_map
from whoosh.qparser import OrGroup, AndGroup, QueryParser
from whoosh.analysis import CharsetFilter, RegexAnalyzer, StopFilter, LowercaseFilter

HERE = os.path.dirname(__file__)
INDEX_PATH_PROVINCIAS = os.path.join(HERE, "..", "data", "index.provincias")
INDEX_PATH_MUNICIPIOS = os.path.join(HERE, "..", "data", "index.municipios")
INDEX_PATH_COMUNIDADES = os.path.join(HERE, "..", "data", "index.comunidades")

INDEX_PATH_PROVINCIAS2COMUNIDADES = os.path.join(HERE, "..", "data", "index.provincias2comunidades")

schema_accents = RegexAnalyzer(r'\w+') | LowercaseFilter() | StopFilter() | CharsetFilter(accent_map)

def _load_generic(f: str) -> Dict[str, list]:
    ret = defaultdict(list)

    with open(f, newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in spamreader:
            code, name = row

            ret[code].append(name)

    return ret

class Search:

    def __init__(self, index_path):
        self.ix = open_dir(index_path)
        self.searcher = self.ix.searcher()

    def search(self, query: str, max_items: int = 10) -> list:

        with self.searcher as searcher:

            if "/" in query:
                group_by = OrGroup
            else:
                group_by = AndGroup

            q = QueryParser("name", self.ix.schema, group=group_by).parse(query)

            ret = searcher.search(q)

            for i in range(max_items):
                try:
                    yield ret[i]

                except IndexError:
                    return

def load_comunidades() -> dict:
    return _load_generic(
        os.path.join(HERE, "../data", "comunidades.with.synonyms.csv")
    )

def load_provincias() -> dict:
    return _load_generic(
        os.path.join(HERE, "../data", "provincias.with.synonyms.csv")
    )

def load_municipios() -> Dict[str, list]:
    ret = defaultdict(list)

    csv_path = os.path.join(HERE, "../data", "municipios.with.synonyms.csv")

    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')

        for row in spamreader:

            cod_comunidad, cod_provincia, cod_municipio, name = row

            cleaned_name = name.split("/")

            for n in cleaned_name:
                loc_code = f"{cod_comunidad}{cod_provincia}{cod_municipio}"

                ret[loc_code].append(
                    (cod_comunidad, cod_provincia, cod_municipio, n)
                )

    return ret


def indexing_provincias():

    index_folder = INDEX_PATH_PROVINCIAS

    schema = Schema(
        cod_provincia=ID(stored=True),
        name=TEXT(stored=True, analyzer=schema_accents)
    )

    ix = create_in(index_folder, schema)

    writer = ix.writer()

    for cod_provincia, name in load_provincias().items():
        for n in name:
            writer.add_document(cod_provincia=cod_provincia, name=n)

    writer.commit()

def indexing_comunidades():

    index_folder = INDEX_PATH_COMUNIDADES

    schema = Schema(
        cod_comunidad=ID(stored=True),
        name=TEXT(stored=True, analyzer=schema_accents)
    )

    ix = create_in(index_folder, schema)

    writer = ix.writer()

    for cod_comunidad, name in load_comunidades().items():
        for n in name:
            writer.add_document(cod_comunidad=cod_comunidad, name=n)

    writer.commit()

def indexing_municipios():

    index_folder = INDEX_PATH_MUNICIPIOS

    schema = Schema(
        cod_comunidad=ID(stored=True),
        cod_provincia=ID(stored=True),
        cod_municipio=ID(stored=True),
        name=TEXT(stored=True, analyzer=schema_accents)
    )

    ix = create_in(index_folder, schema)

    writer = ix.writer()

    for cod_loc, values in load_municipios().items():
        for v in values:
            cod_comunidad, cod_provincia, cod_municipio, name = v

            writer.add_document(
                cod_comunidad=cod_comunidad,
                cod_provincia=cod_provincia,
                cod_municipio=cod_municipio,
                name=name
            )

    writer.commit()

def main():
    indexing_provincias()
    indexing_comunidades()
    indexing_municipios()

if __name__ == '__main__':
    main()
