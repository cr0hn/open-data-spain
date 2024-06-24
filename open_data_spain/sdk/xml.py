from typing import List

import lxml.html

from lxml.html import tostring


def xfirst(xml_element):
    """Get firt node of and XML element or a string"""
    if not xml_element:
        return ""

    if type(xml_element) is list:
        if len(xml_element) > 0:
            return xml_element[0]
        else:
            return ""

    else:
        return xml_element


def xtext(xml_element) -> str:
    if not xml_element:
        return ""

    xt = xfirst(xml_element)

    if hasattr(xt, "is_text"):
        return str(xt)

    elif type(xt) is lxml.html.HtmlElement:
        return tostring(xt).decode()

    else:
        raise ValueError(xml_element)


def xtext_all(xml_element) -> List[str]:
    if not xml_element:
        return []

    xt = xfirst(xml_element)

    if type(xml_element) is list:
        ret = []

        for e in xml_element:

            if type(e) is lxml.html.HtmlElement:
                ret.append(tostring(e).decode())

            else:
                ret.append(str(e))

        # try:
        #     return [
        #         tostring(x).decode()
        #         for x in xml_element
        #         if hasattr(x, "is_text")
        #     ]
        # except Exception as e:
        #     print(e)

        return ret

    elif hasattr(xt, "is_text"):
        return [str(xt)]

    else:
        raise ValueError(xml_element)


__all__ = ("xfirst", "xtext", "xtext_all")
