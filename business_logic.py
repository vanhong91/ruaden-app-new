### dùng bcrypt và PostgreSQL 

import logging
from typing import Dict, List, Tuple, Optional
from database import DatabaseManager
from utils import to_base, from_base, same_dimension, fmt_qty

logger = logging.getLogger(__name__)

def inventory_as_base(user_id: Optional[int]) -> Dict[Tuple[str, str], float]:
    if not user_id:
        logger.warning("inventory_as_base: No user_id provided.")
        return {}
    # Always fetch fresh inventory from database
    inv = DatabaseManager.list_inventory(user_id)
    logger.info(f"inventory_as_base: Retrieved {len(inv)} inventory items for user_id={user_id}")
    agg: Dict[Tuple[str, str], float] = {}
    for row in inv:
        if not all(key in row for key in ["name", "quantity", "unit"]):
            logger.warning(f"Invalid inventory item for user_id={user_id}: {row}")
            continue
        base_qty, base_unit = to_base(row["quantity"], row["unit"])
        key = (DatabaseManager.normalize_name(row["name"]), base_unit.lower())  # Normalize unit to lowercase
        agg[key] = agg.get(key, 0.0) + base_qty
        logger.debug(f"inventory_as_base: {row['name']} -> {base_qty} {base_unit} (normalized key: {key})")
    return agg

def recipe_feasibility(recipe: Dict, user_id: Optional[int]) -> Tuple[bool, List[Dict]]:
    if not user_id:
        logger.error("recipe_feasibility: No valid user_id")
        return False, []
    if not all(key in recipe for key in ["id", "title", "ingredients"]):
        logger.error(f"recipe_feasibility: Invalid recipe structure: {recipe}")
        return False, []
    inv = inventory_as_base(user_id)
    logger.info(f"Checking feasibility for recipe: {recipe['title']} (id={recipe['id']})")
    shorts = []
    feasible = True
    for r in recipe["ingredients"]:
        if not all(key in r for key in ["name", "quantity", "unit"]):
            logger.warning(f"Invalid ingredient in recipe {recipe['title']}: {r}")
            continue
        name_normalized = DatabaseManager.normalize_name(r["name"])
        needed_base, base_unit = to_base(r["quantity"], r["unit"])
        base_unit = base_unit.lower()  # Ensure unit is lowercase
        have_base = inv.get((name_normalized, base_unit), 0.0)
        logger.debug(f"Ingredient: {r['name']} (normalized: {name_normalized}) | Need: {needed_base} {base_unit} | Have: {have_base} {base_unit}")
        if have_base < needed_base - 1e-6:  # Consistent tolerance
            feasible = False
            missing = needed_base - have_base
            display_missing = from_base(missing, base_unit, r["unit"])
            shorts.append(
                {
                    "name": r["name"],
                    "needed_qty": r["quantity"],
                    "needed_unit": r["unit"],
                    "have_qty": from_base(have_base, base_unit, r["unit"]),
                    "have_unit": r["unit"],
                    "missing_base": missing,
                    "base_unit": base_unit,
                    "missing_qty_disp": display_missing,
                    "missing_unit_disp": r["unit"],
                }
            )
    logger.info(f"Recipe {recipe['title']} feasible: {feasible}, missing ingredients: {len(shorts)}")
    return feasible, shorts

def consume_ingredients_for_recipe(recipe: Dict, user_id: Optional[int]) -> bool:
    if not user_id:
        logger.error("consume_ingredients_for_recipe: No valid user_id")
        return False
    if not all(key in recipe for key in ["id", "title", "ingredients"]):
        logger.error(f"consume_ingredients_for_recipe: Invalid recipe structure: {recipe}")
        return False
    # Re-check feasibility with fresh inventory data
    feasible, shorts = recipe_feasibility(recipe, user_id)
    if not feasible:
        logger.error(f"consume_ingredients_for_recipe: Recipe '{recipe['title']}' not feasible, missing: {[s['name'] for s in shorts]}")
        return False
    try:
        with DatabaseManager.get_db_conn() as conn:
            for r in recipe["ingredients"]:
                if not all(key in r for key in ["name", "quantity", "unit"]):
                    logger.warning(f"Invalid ingredient in recipe {recipe['title']}: {r}")
                    return False
                needed_base, base_unit = to_base(r["quantity"], r["unit"])
                if not DatabaseManager.consume_base(user_id, r["name"], needed_base, base_unit.lower(), conn=conn):
                    logger.error(f"Failed to consume {r['name']} ({needed_base} {base_unit}) for recipe '{recipe['title']}'")
                    conn.rollback()
                    return False
            conn.commit()
        logger.info(f"Successfully consumed ingredients for recipe '{recipe['title']}' (id={recipe['id']})")
        return True
    except Exception as e:
        logger.error(f"Error consuming ingredients for recipe '{recipe['title']}': {e}")
        return False