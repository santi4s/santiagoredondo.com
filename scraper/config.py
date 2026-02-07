"""Configuración de consolas y parámetros del scraper."""

CONSOLES = {
    "nes": {
        "display_name": "NES",
        "search_queries": [
            "consola NES",
            "Nintendo NES consola",
        ],
        "exclude_terms": ["mini", "classic", "mando", "juego", "cartucho", "funda", "cable",
                          "camiseta", "poster", "libro", "llavero", "pegatina", "3d", "lampara",
                          "figura", "taza", "vinilo", "pin"],
        "min_price": 15,
        "max_price": 500,
    },
    "snes": {
        "display_name": "Super Nintendo",
        "search_queries": [
            "Super Nintendo consola",
            "SNES consola",
        ],
        "exclude_terms": ["mini", "classic", "mando", "juego", "cartucho", "funda", "cable",
                          "camiseta", "poster", "libro", "llavero", "pegatina", "3d", "lampara",
                          "figura", "taza", "vinilo", "pin"],
        "min_price": 20,
        "max_price": 600,
    },
    "gameboy": {
        "display_name": "Game Boy",
        "search_queries": [
            "Game Boy consola",
            "Game Boy original",
            "Nintendo Game Boy",
        ],
        "exclude_terms": ["color", "advance", "sp", "micro", "juego", "funda", "carcasa",
                          "camiseta", "poster", "libro", "llavero", "pegatina", "3d", "lampara",
                          "figura", "taza", "vinilo", "pin", "cartucho", "cable"],
        "min_price": 10,
        "max_price": 300,
    },
    "gameboy-color": {
        "display_name": "Game Boy Color",
        "search_queries": [
            "Game Boy Color consola",
            "Game Boy Color",
        ],
        "exclude_terms": ["advance", "sp", "juego", "funda", "carcasa",
                          "camiseta", "poster", "libro", "llavero", "pegatina", "3d", "lampara",
                          "figura", "taza", "vinilo", "pin", "cartucho", "cable"],
        "min_price": 15,
        "max_price": 350,
    },
    "mastersystem": {
        "display_name": "Master System",
        "search_queries": [
            "Master System consola",
            "Sega Master System",
        ],
        "exclude_terms": ["II", "2", "mando", "juego", "cartucho", "cable",
                          "camiseta", "poster", "libro", "llavero", "pegatina", "3d", "lampara",
                          "figura", "taza", "vinilo", "pin"],
        "min_price": 15,
        "max_price": 400,
    },
    "mastersystem-2": {
        "display_name": "Master System II",
        "search_queries": [
            "Master System II consola",
            "Master System 2 consola",
            "Sega Master System II",
        ],
        "exclude_terms": ["mando", "juego", "cartucho", "cable",
                          "camiseta", "poster", "libro", "llavero", "pegatina", "3d", "lampara",
                          "figura", "taza", "vinilo", "pin"],
        "min_price": 15,
        "max_price": 400,
    },
    "megadrive": {
        "display_name": "Mega Drive",
        "search_queries": [
            "Mega Drive consola",
            "Sega Mega Drive consola",
        ],
        "exclude_terms": ["II", "2", "mini", "mando", "juego", "cartucho", "cable",
                          "camiseta", "poster", "libro", "llavero", "pegatina", "3d", "lampara",
                          "figura", "taza", "vinilo", "pin"],
        "min_price": 15,
        "max_price": 400,
    },
    "megadrive-2": {
        "display_name": "Mega Drive II",
        "search_queries": [
            "Mega Drive 2 consola",
            "Mega Drive II consola",
            "Sega Mega Drive 2",
        ],
        "exclude_terms": ["mini", "mando", "juego", "cartucho", "cable",
                          "camiseta", "poster", "libro", "llavero", "pegatina", "3d", "lampara",
                          "figura", "taza", "vinilo", "pin"],
        "min_price": 15,
        "max_price": 400,
    },
}

# Centro de España para búsqueda amplia
DEFAULT_LATITUDE = 40.4168
DEFAULT_LONGITUDE = -3.7038
DEFAULT_DISTANCE_KM = 200

# Límites del scraper
MAX_PAGES_PER_QUERY = 5  # ~20 items/página = ~100 items por query
REQUEST_DELAY_MIN = 2.0
REQUEST_DELAY_MAX = 5.0
