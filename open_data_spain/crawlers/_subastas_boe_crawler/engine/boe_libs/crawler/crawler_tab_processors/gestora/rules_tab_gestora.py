from sdk.html import html_to_text
from sdk.regex import regex_engine
from sdk.text import text_remove_spaces


# -------------------------------------------------------------------------
# Información gestora
# -------------------------------------------------------------------------
def g_codigo(html) -> dict:
    if found := regex_engine.search("código", html):

        return {
            "codigo": found.lower().strip().replace(" ", ""),
            "codigo_raw": found
        }

    else:

        return {
            "codigo": None,
            "codigo_raw": None
        }


def g_descripcion(html: str) -> dict:
    if found := regex_engine.search("descripción", html):
        return {
            "descripcion": html_to_text(found).replace("\n", ""),
            "descripcion_raw": found
        }

    else:
        return {
            "descripcion": None,
            "descripcion_raw": None
        }


def g_direccion(html: str) -> dict:
    if found := regex_engine.search("descripción", html):
        return {
            "direccion": text_remove_spaces(found.strip()),
            "direccion_raw": found
        }

    else:
        return {
            "direccion": None,
            "direccion_raw": None
        }


def g_telefono(html: str) -> dict:
    if found := regex_engine.search("teléfono", html):
        return {
            "telefono": found.lower().strip().replace(" ", ""),
            "telefono_raw": found
        }

    else:
        return {
            "telefono": None,
            "telefono_raw": None
        }


def g_fax(html: str) -> dict:
    if found := regex_engine.search("fax", html):
        return {
            "fax": found.lower().strip().replace(" ", ""),
            "fax_raw": found
        }

    else:
        return {
            "fax": None,
            "fax_raw": None
        }


def g_email(html: str) -> dict:
    if found := regex_engine.search("correo", html):
        clean_data = found.lower().strip().replace(" ", "")

        if "@" in clean_data:
            return {
                "email": clean_data,
                "email_raw": found
            }

        else:
            return {
                "email": None,
                "email_raw": found
            }

    else:
        return {
            "email": None,
            "email_raw": None
        }


RULES_TAB_GESTORA = (g_codigo, g_descripcion, g_direccion, g_telefono, g_fax, g_email)

__all__ = ("RULES_TAB_GESTORA",)
