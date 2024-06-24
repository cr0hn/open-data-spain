from typing import Iterable

from dictionary_search import search_all


def find_in_dict(dictionary: dict, keys: str | Iterable[str]) -> Iterable[dict]:
    if type(keys) is str:
        keys = [keys]

    for k in keys:
        for found in search_all(dictionary, k, path_as_string=False):
            yield found


def find_values_in_dict(dictionary: dict, keys: str | Iterable[str]) -> Iterable[str]:
    for _, value in find_in_dict(dictionary, keys):

        if not value:
            continue

        yield value


__all__ = ("find_in_dict", "find_values_in_dict")
