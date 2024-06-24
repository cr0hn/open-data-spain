import os
import re
import jsonschema_rs

REGEX_ID_SUBASTA_URL = re.compile(r'''(idSub=)([\w\-_]+)''')


def subasta_id_from_url(url: str) -> str:
    return REGEX_ID_SUBASTA_URL.search(url).group(2)


def eliminar_nulos(d: dict) -> dict:
    return {k: v for k, v in d.items() if v}


def load_json_schema() -> jsonschema_rs.JSONSchema:
    here = os.path.dirname(__file__)

    with open(os.path.join(here, "subasta.json-schema.json")) as f:
        return jsonschema_rs.JSONSchema.from_str(f.read())


__all__ = ("subasta_id_from_url", "eliminar_nulos", "load_json_schema")
