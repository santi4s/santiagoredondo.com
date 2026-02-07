"""Orquestador principal del scraper de Wallapop para consolas retro."""

import json
import os
import sys
from datetime import datetime, timezone

from config import CONSOLES
from utils import apply_filters, calculate_stats, random_delay
from wallapop_api import scrape_console_api

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "consolas-retro", "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
LATEST_FILE = os.path.join(DATA_DIR, "latest.json")


def scrape_console(console_key, console_config):
    """Scrapea una consola: primero API, si falla usa Selenium."""
    print(f"  Intentando API...")
    items = scrape_console_api(console_config)

    if items is None:
        print(f"  API falló, usando Selenium como respaldo...")
        try:
            from wallapop_selenium import scrape_console_selenium
            items = scrape_console_selenium(console_config)
        except Exception as e:
            print(f"  Selenium también falló: {e}")
            items = []

    # Aplicar filtros de título y precio
    filtered = [item for item in items if apply_filters(item, console_config)]
    print(f"  {len(items)} items raw -> {len(filtered)} tras filtros")
    return filtered


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"=== Scraper Wallapop Consolas Retro - {today} ===\n")

    os.makedirs(DATA_DIR, exist_ok=True)

    daily_snapshot = {
        "date": today,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "consoles": {},
    }

    for console_key, console_config in CONSOLES.items():
        print(f"\n[{console_config['display_name']}]")
        items = scrape_console(console_key, console_config)
        stats = calculate_stats(items)
        daily_snapshot["consoles"][console_key] = stats
        print(f"  Resultado: {stats['available_count']} activos, "
              f"{stats['sold_count']} vendidos, "
              f"precio medio oferta: {stats['avg_offer_price']} EUR")

    # Guardar snapshot del día
    with open(LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(daily_snapshot, f, indent=2, ensure_ascii=False)
    print(f"\nGuardado latest.json")

    # Añadir al histórico
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)

    # Reemplazar si ya existe entrada del mismo día
    history = [entry for entry in history if entry["date"] != today]
    history.append(daily_snapshot)
    history.sort(key=lambda x: x["date"])

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"Guardado history.json ({len(history)} días)")

    print(f"\n=== Scraper completado ===")


if __name__ == "__main__":
    main()
