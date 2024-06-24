import os
import pickle

from typing import Iterable, List, Tuple
from dataclasses import dataclass

from whoosh.index import open_dir
from whoosh.qparser import QueryParser, OrGroup, AndGroup

HERE = os.path.dirname(__file__)

@dataclass
class SimpleResults:
    code: str
    name: str

@dataclass
class MunicipiosResult:
    cod_provincia: str
    cod_comunidad: str
    cod_municipio: str
    name: str

    @property
    def code(self):
        return f"{self.cod_comunidad}{self.cod_provincia}{self.cod_municipio}"

class Container:

    def __init__(self):
        self.items = []

    @property
    def count(self) -> int:
        return len(self.items)

    def add(self, item):
        self.items.append(item)

    def first(self) -> MunicipiosResult or SimpleResults:
        if not self.items:
            return

        else:
            return self.items[0]

    def __iter__(self):
        return self.items.__iter__()

class _Geography:

    def __init__(self):
        self._db_municipios =  None
        self._db_provincias =  None
        self._db_comunidades =  None
        self._lookup_comunidades = None
        self._lookup_comunidades2provincias = None
        self._lookup_provincias2comunidades = None

    def _search_(self, db: str, query: str, max_items: int = 5) -> Iterable[dict]:

        dbs = {
            "municipios": self.db_municipios,
            "provincias": self.db_provincias,
            "comunidades": self.db_comunidades,
        }

        try:
            ix = dbs[db]
        except KeyError:
            raise ValueError(f"Invalid DB value. Allowed values are: "
                       f"'{','.join(dbs.keys())}'")

        with ix.searcher() as searcher:

            if "/" in query:
                group_by = OrGroup
            else:
                group_by = AndGroup

            q = QueryParser("name", ix.schema, group=group_by).parse(query)

            ret = searcher.search(q)

            for i in range(max_items):
                try:
                    yield ret[i]

                except IndexError:
                    return

    def search_municipios(self, query: str, max_results: int = 5) -> Container:
        c = Container()

        places = (
            "municipios",
            "provincias",
            "comunidades"
        )

        for p in places:
            for item in self._search_(p, query.lower(), max_results):
                c.add(MunicipiosResult(
                    cod_municipio=item.get("cod_municipio", None),
                    cod_comunidad=item.get("cod_comunidad", None),
                    cod_provincia=item.get("cod_provincia", None),
                    name=item["name"]
                ))

            if c.count > 0:
                return c

        return c

    def _search_prov_com_(self, prob_com: str, query: str, max_results: int = 5) -> Container:

        code_map = {
            "provincias": "cod_provincia",
            "comunidades": "cod_comunidad"
        }

        code_name = code_map[prob_com]

        c = Container()

        for item in self._search_(prob_com, query, max_results):
            c.add(SimpleResults(
                code=item[code_name],
                name=item["name"]
            ))

        return c

    def search_comunidades(self, query: str, max_results: int = 5) -> Container:
        return self._search_prov_com_("comunidades", query, max_results)

    def search_provincias(self, query: str, max_results: int = 5) -> Container:
        return self._search_prov_com_("provincias", query, max_results)

    @property
    def db_municipios(self):
        if not self._db_municipios:
            self._db_municipios = open_dir(
                os.path.join(HERE, "data", "index.municipios")
            )
        return self._db_municipios

    @property
    def db_provincias(self):
        if not self._db_provincias:
            self._db_provincias = open_dir(
                os.path.join(HERE, "data", "index.provincias")
            )
        return self._db_provincias

    @property
    def db_comunidades(self):
        if not self._db_comunidades:
            self._db_comunidades = open_dir(
                os.path.join(HERE, "data", "index.comunidades")
            )
        return self._db_comunidades

    def lookup_comunidades(self, cod_comunidad: str) -> List[str] | None:
        if not self._lookup_comunidades:
            self._lookup_comunidades = pickle.load(
                open(os.path.join(HERE, "data", "lookups", "comunidades.bin"), "rb")
            )

        return self._lookup_comunidades.get(cod_comunidad, None)

    def lookup_comunidades2provincias(self, cod_comunidad: str) -> List[Tuple[str, str]] | None:
        """
        >>> g = _Geography()
        >>> g.lookup_comunidades2provincias("08")
        [('02', 'Albacete'), ('13', 'Ciudad Real')...]
        """
        if not self._lookup_comunidades2provincias:
            self._lookup_comunidades2provincias = pickle.load(
                open(os.path.join(HERE, "data", "lookups", "comunidades2provincias.bin"), "rb")
            )

        return self._lookup_comunidades2provincias.get(cod_comunidad, None)

    def lookup_provincias2comunidades(self, cod_provincia: str) -> List[Tuple[str, str]] | None:
        """
        >>> g = _Geography()
        >>> g.lookup_provincias2comunidades("02")  # Albacete
        [('08', 'Castilla-La Mancha')]
        >>> g.lookup_provincias2comunidades("01")  # Araba
        [('16', 'País Vasco'), ('16', 'Euskadi')]
        """
        if not self._lookup_provincias2comunidades:
            self._lookup_provincias2comunidades = pickle.load(
                open(os.path.join(HERE, "data", "lookups", "provincia2comunidades.bin"), "rb")
            )

        return self._lookup_provincias2comunidades.get(cod_provincia, None)

Geography = _Geography()

__all__ = ("Geography", "MunicipiosResult")

if __name__ == '__main__':

    import json

    data = json.load(open("spiders_alerts.json", "r"))

    for d in data:
        message = d["message"]
        keyword = d["context"]["text"]

        if message != "No se ha concordancia con el nombre de municipio":
            continue

        try:
            if found := Geography.search_municipios(keyword):
                print("Found!")
            else:
                print(f"Not found for: {keyword}")

        except Exception as e:
            print(d)


