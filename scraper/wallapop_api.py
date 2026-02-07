"""Scraper de Wallapop vía API v3 (método primario)."""

import time
import requests
from config import DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_DISTANCE_KM, MAX_PAGES_PER_QUERY
from utils import random_delay

WALLAPOP_API_BASE = "https://api.wallapop.com/api/v3"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def search_items(keywords, latitude=DEFAULT_LATITUDE, longitude=DEFAULT_LONGITUDE,
                 distance_km=DEFAULT_DISTANCE_KM, start=0):
    """Busca items en la API de Wallapop."""
    url = f"{WALLAPOP_API_BASE}/general/search"
    params = {
        "keywords": keywords,
        "latitude": latitude,
        "longitude": longitude,
        "distance_in_km": distance_km,
        "filters_source": "search_box",
        "order_by": "most_relevance",
        "start": start,
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-ES,es;q=0.9",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
    }

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def classify_item(raw_item):
    """Extrae los campos relevantes de un item de la API."""
    content = raw_item.get("content", raw_item)
    flags = content.get("flags", {})
    return {
        "id": content.get("id", ""),
        "title": content.get("title", ""),
        "price": float(content.get("price", 0)),
        "is_sold": flags.get("sold", False),
        "is_reserved": flags.get("reserved", False),
        "currency": content.get("currency", "EUR"),
    }


def scrape_console_api(console_config):
    """Scrapea todos los items de una consola usando la API.

    Returns:
        list[dict]: Lista de items deduplicados, o None si la API falla.
    """
    all_items = {}

    for query in console_config["search_queries"]:
        print(f"    API: buscando '{query}'...")
        try:
            for page in range(MAX_PAGES_PER_QUERY):
                data = search_items(keywords=query, start=page * 20)

                items_list = data.get("search_objects", data.get("items", []))
                if not items_list:
                    break

                for raw_item in items_list:
                    item = classify_item(raw_item)
                    if item["id"] and item["id"] not in all_items:
                        all_items[item["id"]] = item

                # Si hay menos de 20 items, no hay más páginas
                if len(items_list) < 20:
                    break

                random_delay()

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "?"
            print(f"    API error HTTP {status} para '{query}': {e}")
            if status in (403, 429):
                print("    API bloqueada, se usará Selenium como respaldo")
                return None
            continue
        except Exception as e:
            print(f"    API error para '{query}': {e}")
            return None

        random_delay()

    return list(all_items.values())
