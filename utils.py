### dùng bcrypt và PostgreSQL 

import logging
from typing import Tuple, Optional
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)

# Conversion factors to base units (base units are: g for weight, ml for volume, piece for count)
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

VALID_UNITS = []
for dimension in UNIT_ALIASES.values():
    VALID_UNITS.extend([alias for alias, _ in dimension.items()])

def validate_unit(unit: str) -> bool:
    """Check if a unit is valid."""
    if not unit or not isinstance(unit, str):
        logger.warning(f"Invalid unit: {unit}")
        return False
    unit = unit.strip().lower()
    is_valid = unit in VALID_UNITS
    if not is_valid:
        logger.warning(f"Unit '{unit}' is not in VALID_UNITS")
    return is_valid

def normalize_unit(unit: str) -> Tuple[str, str]:
    """Return dimension and normalized base unit."""
    if not unit or not isinstance(unit, str):
        logger.warning(f"Invalid unit: {unit}")
        return "count", "piece"
    unit = unit.strip().lower()
    for dimension, units in UNIT_ALIASES.items():
        if unit in units:
            return dimension, units[unit][0]
    logger.warning(f"Unrecognized unit '{unit}', defaulting to 'piece'")
    return "count", "piece"

def to_base(quantity: float, unit: str) -> Tuple[float, str]:
    """Convert quantity to base unit."""
    try:
        quantity = float(quantity)
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        dimension, base_unit = normalize_unit(unit)
        for units in UNIT_ALIASES[dimension].values():
            if units[0] == base_unit:
                factor = units[1]
                return round(quantity * factor, 6), base_unit
        logger.error(f"Unit '{unit}' not found in {dimension}")
        return quantity, base_unit
    except (ValueError, TypeError) as e:
        logger.error(f"Error converting {quantity} {unit} to base: {e}")
        return 0.0, "piece"

def from_base(base_qty: float, base_unit: str, target_unit: str) -> float:
    """Convert from base unit to target unit."""
    try:
        base_qty = float(base_qty)
        if base_qty < 0:
            raise ValueError("Quantity cannot be negative")
        dimension, norm_base_unit = normalize_unit(base_unit)
        target_dimension, _ = normalize_unit(target_unit)
        if dimension != target_dimension:
            logger.error(f"Cannot convert between dimensions: {base_unit} ({dimension}) to {target_unit} ({target_dimension})")
            return base_qty
        for unit, (base, factor) in UNIT_ALIASES[dimension].items():
            if unit.lower() == target_unit.lower():
                return float(Decimal(str(base_qty / factor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        logger.error(f"Target unit '{target_unit}' not found in {dimension}")
        return base_qty
    except (ValueError, TypeError) as e:
        logger.error(f"Error converting {base_qty} {base_unit} to {target_unit}: {e}")
        return 0.0

def same_dimension(unit1: str, unit2: str) -> bool:
    """Check if two units are of the same dimension."""
    dim1, _ = normalize_unit(unit1)
    dim2, _ = normalize_unit(unit2)
    return dim1 == dim2

def fmt_qty(qty: float) -> str:
    """Format quantity for display."""
    try:
        return str(Decimal(str(qty)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    except (ValueError, TypeError):
        logger.error(f"Error formatting quantity {qty}")
        return "0.0"