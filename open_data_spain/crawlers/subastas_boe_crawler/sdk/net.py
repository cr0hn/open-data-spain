import os
import time
import random
import logging

from typing import Tuple
from urllib.parse import urlencode

import requests

from lxml.html import fromstring

log = logging.getLogger("ods")


class PlakRequestTimeoutException(Exception):
    pass


def download_and_parse(url: str):
    retires = 0
    max_retries = 20

    while 1:
        try:
            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                raise ValueError(f"Downloading '{url}' failed with status code {response.status_code}")

            content = response.content

            break

        except Exception as e:
            retires += 1

            if max_retries <= retires:
                raise RuntimeError(str(e))

            time.sleep(random.randint(1, 3))

    xml_parsed = fromstring(content)

    return xml_parsed, content

#
# def make_request(url: str, params: dict = None, timeout: int = 50, retries: int = 3) -> Tuple[int, str]:
#     if params is None:
#         params = {}
#
#     use_scraping_proxy = False
#
#     # Using proxy service:
#     ## scrapingrobot
#     if scrapingrobot_token := os.getenv("SCRAPINGROBOT_TOKEN"):
#         use_scraping_proxy = True
#
#         real_query = f"{url}?{urlencode(params)}"
#
#         new_url = f"https://api.scrapingrobot.com/v1/proxy?token={scrapingrobot_token}&url={real_query}"
#
#         config = dict(
#             url=new_url,
#             headers={"accept": "application/json"},
#             timeout=timeout,
#         )
#
#     else:
#         # Checks for proxies
#         proxies = {}
#
#         if proxy := os.environ.get("CUSTOM_HTTP_PROXY"):
#             proxies["http"] = proxy
#
#         if proxy := os.environ.get("CUSTOM_HTTPS_PROXY"):
#             proxies["https"] = proxy
#
#         config = dict(
#             url=url,
#             params=params,
#             timeout=timeout,
#             proxies=proxies
#         )
#
#     current_tries = 0
#
#     while 1:
#         try:
#             response = requests.get(**config)
#
#             if use_scraping_proxy:
#                 try:
#                     return response.json()["httpCode"], response.json()["result"]
#                 except Exception as e:
#                     try:
#                         notify_pushover("Crétitos de Scraping Robot", f"Se han acabado los créditos de scrapingrobot: {e}")
#                     except Exception as e:
#                         log.exception(f"Error al enviar notificación: {e}", exc_info=True, stack_info=True)
#                     exit(1)
#
#             else:
#                 return response.status_code, response.content.decode()
#
#         except requests.exceptions.ReadTimeout:
#             log.debug("    !> Error de lectura en el catastro. Reintentando...")
#             time.sleep(random.randint(1, 3))
#             current_tries += 1
#
#             if current_tries >= retries:
#                 raise PlakRequestTimeoutException("Tiempo de espera agotado")


__all__ = ("download_and_parse", "make_request")
