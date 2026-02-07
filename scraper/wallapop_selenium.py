"""Scraper de Wallapop vía Selenium (método de respaldo)."""

import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import random_delay

WALLAPOP_SEARCH_URL = "https://es.wallapop.com/app/search"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def create_driver():
    """Crea un driver de Chrome headless con opciones anti-detección."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver


def _accept_cookies(driver):
    """Acepta el banner de cookies si aparece."""
    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_btn.click()
        time.sleep(1)
    except Exception:
        pass


def _scroll_page(driver, max_scrolls=8):
    """Hace scroll para cargar más resultados."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1.5, 3.0))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def _parse_price(price_text):
    """Convierte texto de precio a float."""
    cleaned = re.sub(r"[^\d,.]", "", price_text)
    cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _extract_items(driver):
    """Extrae items de la página actual."""
    items = []

    # Wallapop usa diferentes selectores según la versión.
    # Probamos varios patrones comunes.
    card_selectors = [
        "tsl-public-card",
        "[class*='ItemCard']",
        "a[href*='/item/']",
    ]

    cards = []
    for selector in card_selectors:
        cards = driver.find_elements(By.CSS_SELECTOR, selector)
        if cards:
            break

    for card in cards:
        try:
            # Intentar extraer título
            title = ""
            for title_sel in ["[class*='title']", "p", "span"]:
                try:
                    el = card.find_element(By.CSS_SELECTOR, title_sel)
                    if el.text.strip():
                        title = el.text.strip()
                        break
                except Exception:
                    continue

            # Intentar extraer precio
            price = 0.0
            for price_sel in ["[class*='price']", "[class*='Price']"]:
                try:
                    el = card.find_element(By.CSS_SELECTOR, price_sel)
                    if el.text.strip():
                        price = _parse_price(el.text)
                        break
                except Exception:
                    continue

            # Detectar vendido/reservado
            is_sold = False
            is_reserved = False
            try:
                card_text = card.text.lower()
                is_sold = "vendido" in card_text
                is_reserved = "reservado" in card_text
            except Exception:
                pass

            # Extraer ID del href si es posible
            item_id = ""
            try:
                href = card.get_attribute("href") or ""
                if "/item/" in href:
                    item_id = href.split("/item/")[-1].split("?")[0].split("/")[0]
            except Exception:
                pass

            if title and price > 0:
                # Usar ID real si existe, si no generar clave por título+precio
                dedup_id = item_id or f"{title}_{price}"
                items.append({
                    "id": dedup_id,
                    "title": title,
                    "price": price,
                    "is_sold": is_sold,
                    "is_reserved": is_reserved,
                    "currency": "EUR",
                })
        except Exception:
            continue

    return items


def scrape_console_selenium(console_config):
    """Scrapea todos los items de una consola usando Selenium.

    Returns:
        list[dict]: Lista de items deduplicados.
    """
    all_items = {}
    driver = None

    try:
        driver = create_driver()

        for query in console_config["search_queries"]:
            print(f"    Selenium: buscando '{query}'...")
            try:
                url = f"{WALLAPOP_SEARCH_URL}?keywords={query}"
                driver.get(url)
                time.sleep(random.uniform(3, 5))

                _accept_cookies(driver)
                _scroll_page(driver)

                items = _extract_items(driver)
                for item in items:
                    if item["id"] not in all_items:
                        all_items[item["id"]] = item

                print(f"    Selenium: {len(items)} items encontrados para '{query}'")
                random_delay()

            except Exception as e:
                print(f"    Selenium error para '{query}': {e}")
                continue

    except Exception as e:
        print(f"    Selenium error general: {e}")
    finally:
        if driver:
            driver.quit()

    return list(all_items.values())
