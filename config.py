# config.py
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_NAME = os.getenv("SQLITE_DB_PATH", os.path.abspath("data.db"))

# Application titles
APP_TITLE_EN = "What to Cook Today"
APP_TITLE_VI = "Hôm Nay Nấu Gì"

# Centralized unit aliases and valid units
UNIT_ALIASES = {
    "weight": {
        "g": ("g", 1.0),
        "gram": ("g", 1.0),
        "grams": ("g", 1.0),
        "kg": ("g", 1000.0),
        "kilogram": ("g", 1000.0),
        "kilograms": ("g", 1000.0),
        "lạng": ("g", 100.0),
        "lang": ("g", 100.0),
        "ounce": ("g", 28.3495),
        "ounces": ("g", 28.3495),
        "pound": ("g", 453.592),
        "pounds": ("g", 453.592),
    },
    "volume": {
        "ml": ("ml", 1.0),
        "milliliter": ("ml", 1.0),
        "milliliters": ("ml", 1.0),
        "l": ("ml", 1000.0),
        "liter": ("ml", 1000.0),
        "liters": ("ml", 1000.0),
        "tsp": ("ml", 4.92892),
        "teaspoon": ("ml", 4.92892),
        "teaspoons": ("ml", 4.92892),
        "tbsp": ("ml", 14.7868),
        "tablespoon": ("ml", 14.7868),
        "tablespoons": ("ml", 14.7868),
        "cup": ("ml", 236.588),
        "cups": ("ml", 236.588),
        "chén": ("ml", 200.0),  # Vietnamese small bowl
        "chen": ("ml", 200.0),
        "bát": ("ml", 500.0),  # Vietnamese bowl
        "bat": ("ml", 500.0),
    },
    "count": {
        "piece": ("piece", 1.0),
        "pieces": ("piece", 1.0),
        "pc": ("piece", 1.0),
        "pcs": ("piece", 1.0),
        "cái": ("piece", 1.0),
        "cai": ("piece", 1.0),
        "cai.": ("piece", 1.0),
    }
}

VALID_UNITS = list(set(alias for dimension in UNIT_ALIASES.values() for alias in dimension.keys()))