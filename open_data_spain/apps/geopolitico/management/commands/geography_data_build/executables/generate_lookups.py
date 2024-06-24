import csv
import os
import pickle
from collections import defaultdict
from typing import Dict, List

PICKLED_BASE_PATH = "../data/lookups"
HERE = os.path.dirname(os.path.abspath(__file__))


def comunidades2provincias(f: str):
    ret = defaultdict(list)

    with open(f, newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')

        for row in spamreader:
            comunidad, provincia, name = row

            ret[comunidad].append((provincia, name))

    return ret


def comunidades(comunidades: str) -> Dict[str, List[str]]:
    ret = defaultdict(list)

    with open(comunidades, newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in spamreader:
            comunidad, name = row

            ret[comunidad].append(name)

    return ret


def provincias2comunidades(c2p: Dict[str, List[str]], c, comunidades: str):
    ret = defaultdict(list)

    already_inserted = set()

    with open(comunidades, "r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in spamreader:
            provincia_cod, provincia_name = row

            for comunidad_code, data in c2p.items():
                for prov, name in data:

                    if prov == provincia_cod:
                        for comunidad_name in c[comunidad_code]:

                            key = f"{provincia_cod}{comunidad_code}{comunidad_name}"

                            if key not in already_inserted:
                                ret[provincia_cod].append((comunidad_code, comunidad_name))
                                already_inserted.add(key)

    return ret


def main():
    c = comunidades(os.path.abspath(os.path.join(HERE, "../data/comunidades.with.synonyms.csv")))
    c2p = comunidades2provincias(os.path.abspath(os.path.join(HERE, "../data/provincias_and_comunidades.with.synonyms.csv")))
    p2c = provincias2comunidades(c2p, c, os.path.abspath(os.path.join(HERE, "../data/provincias.with.synonyms.csv")))

    pickle.dump(
        c,
        open(os.path.join(PICKLED_BASE_PATH, "comunidades.bin"), "wb"),
        protocol=pickle.HIGHEST_PROTOCOL
    )
    pickle.dump(
        c2p,
        open(os.path.join(PICKLED_BASE_PATH, "comunidades2provincias.bin"), "wb"),
        protocol=pickle.HIGHEST_PROTOCOL
    )
    pickle.dump(
        p2c,
        open(os.path.join(PICKLED_BASE_PATH, "provincia2comunidades.bin"), "wb"),
        protocol=pickle.HIGHEST_PROTOCOL
    )

    print("examples")
    print(p2c["01"])


if __name__ == '__main__':
    main()
