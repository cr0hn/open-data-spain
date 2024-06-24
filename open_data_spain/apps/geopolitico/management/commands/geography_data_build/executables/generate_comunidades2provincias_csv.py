import csv

from typing import Tuple, List


def _load_provincia2municipios(f: str) -> List[Tuple[str, str]]:
    ret = []

    with open(f, newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')

        for row in spamreader:
            comunidad, provincia, municipio, name = row

            ret.append((provincia, comunidad))

    return ret


def _load_provincias(f: str) -> List[Tuple[str, str]]:
    ret = []

    with open(f, newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in spamreader:
            provincia, name = row

            ret.append((provincia, name))

    return ret


def main():
    provincia2municipios = _load_provincia2municipios("../data/municipios.with.synonyms.csv")
    provincias = _load_provincias("../data/provincias.with.synonyms.csv")

    processed = set()

    with open("../data/provincias_and_comunidades.with.synonyms.csv", "w", ) as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';', quotechar='"')

        for provincia_code2, provincia_name in provincias:
            for provincia_code, comunidad in provincia2municipios:
                if provincia_code2 == provincia_code:
                    key = f"{comunidad}{provincia_code}{provincia_name}"

                    if key not in processed:
                        csv_writer.writerow([comunidad, provincia_code, provincia_name])
                        processed.add(key)


if __name__ == '__main__':
    main()
