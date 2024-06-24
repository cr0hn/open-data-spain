import html2text as h2t


def html_to_text(html: str) -> str:
    h = h2t.HTML2Text()
    h.ignore_emphasis = True
    h.ignore_links = True

    return h.handle(html).strip(" \n")


__all__ = ("html_to_text",)
