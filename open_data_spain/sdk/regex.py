import re
import hashlib
import html as html_module

REGEX_SPACES = re.compile("\s")
REGEX_PRICE = re.compile(r"([\d.,]{3,20})")
REGEX_MULTIPLE_SPACES = re.compile("\s\s+")
REGEX_PARENTHESIS_OPEN = re.compile(r"\( +")
REGEX_PARENTHESIS_CLOSE = re.compile(r" \)+")
REGEX_CRU = re.compile(r'\d{14}', re.IGNORECASE)
REGEX_50_PORCIENTO = re.compile(r'50.*%', re.IGNORECASE)
REGEX_FECHAS = re.compile(r'''\d{1,2}[-/]\d{1,2}[-/]\d{2,4}''')
REGEX_REFERENCIA_CATASTRAL = re.compile(r'[\w]{20}', re.IGNORECASE)
REGEX_REFERENCIA_CATASTRAL_ALT = re.compile(r'(referencia\s+catastral[:\-]*)([\w\s]+)([.,])', re.IGNORECASE)


class RegexEngine:

    def __init__(self):
        self.regex_cache = {}

    def search(self, text: str, html: str, exact_match: bool = True) -> str | None:
        unescaped_html = html_module.unescape(html)

        if exact_match:
            regex_template = r"(<th>" + text.replace(" ", "[.\s]+") + r"</th>([\.\s]*)(<td>))"

        else:
            regex_template = r"(<th>.*" + text.replace(" ", "[.\s]+") + r".*</th>([\.\s]*)(<td>))"

        regex = self._cache_regex(regex_template)

        if match := regex.search(unescaped_html):
            start = match.end()

            # Buscar el primer <td> hasta </td>
            close_td = unescaped_html[start:].find("</td>")

            return unescaped_html[start:start + close_td]
        else:
            return None

    def _cache_regex(self, regex: str, prefix: str = None):
        if prefix is None:
            prefix = ""

        cache_key = hashlib.sha256(str(f"{prefix}#{regex}").encode("utf-8")).hexdigest()

        try:
            return self.regex_cache[cache_key]
        except KeyError:
            new_regex = re.compile(regex, re.IGNORECASE)
            self.regex_cache[cache_key] = new_regex

            return new_regex


regex_engine = RegexEngine()

__all__ = ("REGEX_SPACES", "REGEX_MULTIPLE_SPACES", "REGEX_FECHAS", "REGEX_REFERENCIA_CATASTRAL",
           "REGEX_REFERENCIA_CATASTRAL_ALT", "REGEX_CRU", "REGEX_50_PORCIENTO", "REGEX_PRICE", "REGEX_PARENTHESIS_OPEN",
           "REGEX_PARENTHESIS_CLOSE", "regex_engine")
