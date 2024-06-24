import datetime

from functools import lru_cache
from typing import List, Iterable

from .html import html_to_text

from .regex import REGEX_PRICE, REGEX_MULTIPLE_SPACES, REGEX_PARENTHESIS_OPEN, REGEX_PARENTHESIS_CLOSE


def extract_first_price(text: str) -> float:
    if p := extract_all_prices(text):
        return p[0]


def extract_all_prices(text: str) -> List[float]:
    def _is_year(t: str) -> bool:

        @lru_cache
        def _latest_years_() -> List[str]:
            return list(str(x) for x in range(1980, datetime.datetime.now().year))

        if t in _latest_years_():
            return True
        else:
            return False

    def _transform_price(t: str) -> str:

        if t.endswith((".", ",")):
            t = t[:-1]

        # 19.123,23
        if "." in t and "," in t:
            return t.replace(".", "").replace(",", ".")

        # 19.123
        elif "." in t:
            return t.replace(".", "")

        # 19123,23
        elif "," in t:
            return t.replace(",", ".")

        # 19123
        else:
            return t

    if not text:
        return []

    plain_text = html_to_text(text)

    if found := REGEX_PRICE.findall(plain_text):
        ret = []

        for m in found:

            proposal_price = _transform_price(m)

            if _is_year(proposal_price):
                continue

            try:
                ret.append(float(proposal_price))
            except Exception:
                continue

        return ret

    else:
        return []


def text_parse_price(text: str) -> float:
    if not text:
        return 0.0

    return float(text.replace("€", "").replace(".", "").strip().replace(",", "."))


def text_remove_spaces(text: str) -> str:
    if not text:
        return ""

    return REGEX_MULTIPLE_SPACES.sub(' ', text)


def text_remove_spaces_in_parenthesis(text: str) -> str:
    if not text:
        return ""

    if "(" in text:
        step1 = REGEX_PARENTHESIS_OPEN.sub("(", text)
    else:
        step1 = text

    if ")" in step1:
        step2 = REGEX_PARENTHESIS_OPEN.sub(")", step1)
    else:
        step2 = step1

    return step2


def search_with_list(value: str, keywords: Iterable[str]) -> bool:
    if any(r in value for r in keywords):
        return True
    else:
        return False


__all__ = ("extract_first_price", "extract_all_prices", "text_parse_price", "text_remove_spaces",
           "text_remove_spaces_in_parenthesis", "search_with_list")
