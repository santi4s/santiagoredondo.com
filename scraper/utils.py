"""Utilidades compartidas del scraper."""

import time
import random
from config import REQUEST_DELAY_MIN, REQUEST_DELAY_MAX


def random_delay():
    """Espera un tiempo aleatorio entre requests."""
    delay = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
    time.sleep(delay)


def apply_filters(item, console_config):
    """Filtra items por título y precio.

    Returns:
        bool: True si el item pasa los filtros.
    """
    title_lower = item.get("title", "").lower()
    price = item.get("price", 0)

    # Filtrar por precio
    if price < console_config.get("min_price", 0):
        return False
    if price > console_config.get("max_price", float("inf")):
        return False

    # Filtrar por términos de exclusión
    for term in console_config.get("exclude_terms", []):
        if term.lower() in title_lower:
            return False

    return True


def calculate_stats(items):
    """Calcula estadísticas agregadas de una lista de items.

    Returns:
        dict: Estadísticas de la consola.
    """
    available = [i for i in items if not i.get("is_sold") and not i.get("is_reserved")]
    sold = [i for i in items if i.get("is_sold")]

    available_prices = [i["price"] for i in available if i.get("price", 0) > 0]
    sold_prices = [i["price"] for i in sold if i.get("price", 0) > 0]

    def safe_avg(prices):
        return round(sum(prices) / len(prices), 2) if prices else None

    def safe_median(prices):
        if not prices:
            return None
        sorted_p = sorted(prices)
        n = len(sorted_p)
        if n % 2 == 0:
            return round((sorted_p[n // 2 - 1] + sorted_p[n // 2]) / 2, 2)
        return round(sorted_p[n // 2], 2)

    return {
        "total_listings": len(items),
        "available_count": len(available),
        "sold_count": len(sold),
        "reserved_count": len([i for i in items if i.get("is_reserved")]),
        "avg_offer_price": safe_avg(available_prices),
        "median_offer_price": safe_median(available_prices),
        "min_offer_price": round(min(available_prices), 2) if available_prices else None,
        "max_offer_price": round(max(available_prices), 2) if available_prices else None,
        "avg_sold_price": safe_avg(sold_prices),
        "median_sold_price": safe_median(sold_prices),
    }
