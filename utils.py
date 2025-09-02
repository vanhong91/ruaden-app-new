# utils.py
import logging
from typing import Tuple
from decimal import Decimal, ROUND_HALF_UP
from config import UNIT_ALIASES, VALID_UNITS

logger = logging.getLogger(__name__)

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

def normalize_name(name: str) -> str:
    """Normalize inventory/recipe names for comparison."""
    return name.strip().lower() if isinstance(name, str) else ""

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
        factor = next((f[1] for u, f in UNIT_ALIASES[dimension].items() if u == unit.lower()), 1.0)
        return round(quantity * factor, 6), base_unit
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
        factor = next((f[1] for u, f in UNIT_ALIASES[dimension].items() if u.lower() == target_unit.lower()), 1.0)
        return float(Decimal(str(base_qty / factor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
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