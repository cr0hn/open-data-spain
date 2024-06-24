import html as html_module

from sdk.xml import xfirst, xtext


def extraer_datos(element, actions) -> dict:
    """
    :param element: Elemento HTML resultado del un xpath
    """
    if not element:
        return {}

    ret = {}

    for el in element.xpath(".//tr"):
        title = xtext(el.xpath(".//th/text()")).lower()
        content = xfirst(el.xpath(".//td"))
        content_text = xtext(el.xpath(".//td/text()"))

        if "\n" in content_text:
            content_text = xtext(el.xpath(".//td"))

        if type(actions) == dict:
            for rules, action in actions:

                if any(r in title for r in rules):

                    if d := action(content_text, content):
                        ret.update(d)
                    break

        elif type(actions) is list:
            for action in actions:
                ret.update(action(content_text, content))

    return ret


def apply_rules(html: str, actions) -> dict:

    ret = {}

    if hasattr(html, "decode"):
        html_1 = html.decode()
    else:
        html_1 = html

    html_2 = html_module.unescape(html_1)

    for action in actions:
        ret.update(action(html_2))

    return ret


__all__ = ("extraer_datos", "apply_rules")
