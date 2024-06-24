from functools import lru_cache

import re

REGEX_ID_SUBASTA_URL = re.compile(r'''(idSub=)([\w\-_]+)''')


def subasta_id_from_url(url: str) -> str:
    return REGEX_ID_SUBASTA_URL.search(url).group(2)


def eliminar_nulos(d: dict) -> dict:
    return {k: v for k, v in d.items() if v}


__all__ = ("subasta_id_from_url", "eliminar_nulos")
