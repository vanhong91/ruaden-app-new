
import sqlite3
from typing import Optional, List, Dict, Any
from config import DB_NAME, VALID_UNITS
import logging
from datetime import datetime
import bcrypt

logger = logging.getLogger(__name__)

class DatabaseManager:
    @staticmethod
    def get_db_conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def init_db():
        """Initialize the database schema if not exists."""
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        security_question TEXT,
                        security_answer TEXT
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        quantity REAL NOT NULL,
                        unit TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS recipes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        title TEXT NOT NULL,
                        category TEXT,
                        instructions TEXT,
                        servings INTEGER DEFAULT 1,
                        is_signature BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ingredients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        recipe_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        quantity REAL NOT NULL,
                        unit TEXT NOT NULL,
                        is_spice BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS cooked_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        recipe_id INTEGER NOT NULL,
                        cooked_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
                    )
                """)
                conn.commit()
                logger.info("Database schema initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            raise

    @staticmethod
    def validate_user_id(user_id: int) -> bool:
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
                return cur.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Error validating user_id {user_id}: {e}")
            return False

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        try:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            raise ValueError(f"Failed to hash password: {e}")

    @staticmethod
    def check_password(stored_hash: str, password: str) -> bool:
        """Verify a password against a stored bcrypt hash."""
        try:
            # Ensure stored_hash is a valid string and likely a bcrypt hash
            if not isinstance(stored_hash, str) or not stored_hash.startswith('$2'):
                logger.error(f"Invalid stored hash format: {stored_hash[:10]}...")
                return False
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        except ValueError as e:
            logger.error(f"Invalid salt or hash: {e} for stored_hash: {stored_hash[:10]}...")
            return False
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False

    @staticmethod
    def create_user(username: str, password: str, sec_question: str, sec_answer: str) -> tuple[bool, str]:
        from utils import normalize_name
        if not all([username, password, sec_question, sec_answer]):
            return False, "All fields are required"
        normalized_username = normalize_name(username)
        try:
            hashed_password = DatabaseManager.hash_password(password)
            hashed_sec_answer = DatabaseManager.hash_password(sec_answer)
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM users WHERE username = ?", (normalized_username,))
                if cur.fetchone():
                    return False, "Username already exists"
                cur.execute(
                    "INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)",
                    (normalized_username, hashed_password, sec_question, hashed_sec_answer)
                )
                conn.commit()
                return True, "User created successfully"
        except (sqlite3.Error, ValueError) as e:
            logger.error(f"Database error creating user {normalized_username}: {e}")
            return False, f"Database error: {str(e)}"

    @staticmethod
    def verify_login(username: str, password: str) -> Optional[int]:
        from utils import normalize_name
        normalized_username = normalize_name(username)
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, password FROM users WHERE username = ?", (normalized_username,))
                row = cur.fetchone()
                if row and DatabaseManager.check_password(row["password"], password):
                    return row["id"]
                return None
        except sqlite3.Error as e:
            logger.error(f"Error verifying login for {normalized_username}: {e}")
            return None

    @staticmethod
    def reset_password(username: str, sec_answer: str, new_password: str) -> bool:
        from utils import normalize_name
        normalized_username = normalize_name(username)
        try:
            hashed_new_password = DatabaseManager.hash_password(new_password)
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT security_answer FROM users WHERE username = ?", (normalized_username,))
                row = cur.fetchone()
                if row and DatabaseManager.check_password(row["security_answer"], sec_answer):
                    cur.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_password, normalized_username))
                    conn.commit()
                    return True
                return False
        except (sqlite3.Error, ValueError) as e:
            logger.error(f"Error resetting password for {normalized_username}: {e}")
            return False

    @staticmethod
    def list_inventory(user_id: int) -> List[Dict]:
        if not DatabaseManager.validate_user_id(user_id):
            logger.error(f"Invalid user_id {user_id}")
            return []
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, name, quantity, unit FROM inventory WHERE user_id = ?", (user_id,))
                return [{"id": row["id"], "name": row["name"], "quantity": row["quantity"], "unit": row["unit"]} for row in cur.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error listing inventory for user_id {user_id}: {e}")
            return []

    @staticmethod
    def upsert_inventory(user_id: int, name: str, quantity: float, unit: str, conn: Optional[sqlite3.Connection] = None) -> bool:
        from utils import validate_unit, normalize_name
        if not DatabaseManager.validate_user_id(user_id):
            logger.error(f"Invalid user_id {user_id}")
            return False
        if not validate_unit(unit):
            logger.error(f"Invalid unit {unit}")
            return False
        normalized_name = normalize_name(name)
        if quantity < 0:
            logger.error("Quantity cannot be negative")
            return False
        close_conn = False
        if conn is None:
            conn = DatabaseManager.get_db_conn()
            close_conn = True
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, quantity FROM inventory WHERE user_id = ? AND name = ? AND unit = ?",
                (user_id, normalized_name, unit.lower())
            )
            row = cur.fetchone()
            if row:
                new_qty = row["quantity"] + quantity
                cur.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (new_qty, row["id"]))
            else:
                cur.execute(
                    "INSERT INTO inventory (user_id, name, quantity, unit) VALUES (?, ?, ?, ?)",
                    (user_id, normalized_name, quantity, unit.lower())
                )
            if close_conn:
                conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Database error upserting inventory for user_id {user_id}, name {normalized_name}: {e}")
            if close_conn:
                conn.rollback()
            return False
        finally:
            if close_conn:
                conn.close()

    @staticmethod
    def delete_inventory(inventory_id: int) -> bool:
        if not isinstance(inventory_id, int) or inventory_id <= 0:
            logger.error(f"Invalid inventory_id {inventory_id}")
            return False
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM inventory WHERE id = ?", (inventory_id,))
                conn.commit()
                return cur.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Error deleting inventory_id {inventory_id}: {e}")
            return False

    @staticmethod
    def consume_base(user_id: int, name: str, base_qty: float, base_unit: str, conn: Optional[sqlite3.Connection] = None) -> bool:
        from utils import to_base, from_base, normalize_name
        if not DatabaseManager.validate_user_id(user_id):
            logger.error(f"Invalid user_id {user_id}")
            return False
        normalized_name = normalize_name(name)
        close_conn = False
        if conn is None:
            conn = DatabaseManager.get_db_conn()
            close_conn = True
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, quantity, unit FROM inventory WHERE user_id = ? AND name = ?",
                        (user_id, normalized_name))
            rows = cur.fetchall()
            remaining = base_qty
            for row in rows:
                item_base_qty, item_base_unit = to_base(row["quantity"], row["unit"])
                if item_base_unit == base_unit and remaining > 0:
                    consume_qty = min(remaining, item_base_qty)
                    new_base_qty = item_base_qty - consume_qty
                    new_qty = from_base(new_base_qty, base_unit, row["unit"])
                    cur.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (new_qty, row["id"]))
                    if new_qty <= 1e-6:
                        cur.execute("DELETE FROM inventory WHERE id = ?", (row["id"],))
                    remaining -= consume_qty
            if remaining > 1e-6:
                logger.error(f"Insufficient {normalized_name}: needed {base_qty} {base_unit}, remaining {remaining}")
                if close_conn:
                    conn.rollback()
                return False
            if close_conn:
                conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error consuming {normalized_name} for user_id {user_id}: {e}")
            if close_conn:
                conn.rollback()
            return False
        finally:
            if close_conn:
                conn.close()

    @staticmethod
    def list_recipes(user_id: int) -> List[Dict]:
        if not DatabaseManager.validate_user_id(user_id):
            logger.error(f"Invalid user_id {user_id}")
            return []
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, title, category, instructions, servings, is_signature FROM recipes WHERE user_id = ?", (user_id,))
                recipes = [{"id": row["id"], "title": row["title"], "category": row["category"],
                            "instructions": row["instructions"], "servings": row["servings"],
                            "is_signature": bool(row["is_signature"])} for row in cur.fetchall()]
                for recipe in recipes:
                    cur.execute("SELECT id, name, quantity, unit, is_spice FROM ingredients WHERE recipe_id = ?",
                                (recipe["id"],))
                    recipe["ingredients"] = [{"id": ing["id"], "name": ing["name"], "quantity": ing["quantity"],
                                             "unit": ing["unit"], "is_spice": bool(ing["is_spice"])} for ing in cur.fetchall()]
                return recipes
        except sqlite3.Error as e:
            logger.error(f"Error listing recipes for user_id {user_id}: {e}")
            return []

    @staticmethod
    def get_recipe(recipe_id: int) -> Optional[Dict]:
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, title, category, instructions, servings, is_signature FROM recipes WHERE id = ?", (recipe_id,))
                row = cur.fetchone()
                if not row:
                    return None
                recipe = {"id": row["id"], "title": row["title"], "category": row["category"],
                          "instructions": row["instructions"], "servings": row["servings"],
                          "is_signature": bool(row["is_signature"])}
                cur.execute("SELECT id, name, quantity, unit, is_spice FROM ingredients WHERE recipe_id = ?",
                            (recipe_id,))
                recipe["ingredients"] = [{"id": ing["id"], "name": ing["name"], "quantity": ing["quantity"],
                                         "unit": ing["unit"], "is_spice": bool(ing["is_spice"])} for ing in cur.fetchall()]
                return recipe
        except sqlite3.Error as e:
            logger.error(f"Error retrieving recipe_id {recipe_id}: {e}")
            return None

    @staticmethod
    def create_recipe_from_table(user_id: int, title: str, category: str, instructions: str, servings: int, is_signature: bool, ingredients: List[Dict]) -> tuple[bool, str]:
        from utils import validate_unit, normalize_name
        if not DatabaseManager.validate_user_id(user_id):
            logger.error(f"Invalid user_id {user_id}")
            return False, "Invalid user ID"
        if not title:
            return False, "Recipe title is required"
        if servings < 1:
            return False, "Servings must be positive"
        valid_ingredients = []
        for ing in ingredients:
            if not all(k in ing for k in ["name", "quantity", "unit"]):
                return False, f"Invalid ingredient: {ing}"
            if not validate_unit(ing["unit"]):
                return False, f"Invalid unit in ingredient: {ing['unit']}"
            if ing["quantity"] <= 0:
                return False, f"Invalid quantity in ingredient: {ing['name']}"
            valid_ingredients.append(ing)
        normalized_title = normalize_name(title)
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO recipes (user_id, title, category, instructions, servings, is_signature) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, normalized_title, category, instructions, servings, int(is_signature))
                )
                recipe_id = cur.lastrowid
                for ing in valid_ingredients:
                    cur.execute(
                        "INSERT INTO ingredients (recipe_id, name, quantity, unit, is_spice) VALUES (?, ?, ?, ?, ?)",
                        (recipe_id, normalize_name(ing["name"]), ing["quantity"], ing["unit"].lower(), ing.get("is_spice", False))
                    )
                conn.commit()
                return True, "Recipe saved successfully"
        except sqlite3.Error as e:
            logger.error(f"Database error saving recipe '{normalized_title}' for user_id {user_id}: {e}")
            return False, f"Database error: {str(e)}"

    @staticmethod
    def delete_recipe(recipe_id: int) -> bool:
        if not isinstance(recipe_id, int) or recipe_id <= 0:
            logger.error(f"Invalid recipe_id {recipe_id}")
            return False
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT title FROM recipes WHERE id = ?", (recipe_id,))
                recipe = cur.fetchone()
                if not recipe:
                    logger.warning(f"No recipe found with id {recipe_id}")
                    return False
                cur.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
                cur.execute("DELETE FROM cooked_history WHERE recipe_id = ?", (recipe_id,))
                cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            logger.error(f"Database error deleting recipe_id {recipe_id}: {e}")
            return False

    @staticmethod
    def log_cooked_recipe(user_id: int, recipe_id: int):
        if not DatabaseManager.validate_user_id(user_id):
            logger.error(f"Invalid user_id {user_id}")
            raise ValueError(f"Invalid user_id {user_id}")
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM recipes WHERE id = ? AND user_id = ?", (recipe_id, user_id))
                if not cur.fetchone():
                    logger.error(f"Invalid recipe_id {recipe_id} for user_id {user_id}")
                    raise ValueError(f"Invalid recipe_id {recipe_id}")
                cur.execute("INSERT INTO cooked_history (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error logging cooked recipe for user_id {user_id}, recipe_id {recipe_id}: {e}")
            raise

    @staticmethod
    def list_cooked_history(user_id: int) -> List[Dict]:
        if not DatabaseManager.validate_user_id(user_id):
            logger.error(f"Invalid user_id {user_id}")
            return []
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, recipe_id, cooked_date FROM cooked_history WHERE user_id = ? ORDER BY cooked_date DESC",
                            (user_id,))
                return [{"id": row["id"], "recipe_id": row["recipe_id"], "cooked_date": str(row["cooked_date"])}
                        for row in cur.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error listing cooked history for user_id {user_id}: {e}")
            return []

    @staticmethod
    def get_cooked_count(user_id: int, recipe_id: int) -> int:
        if not DatabaseManager.validate_user_id(user_id):
            logger.error(f"Invalid user_id {user_id}")
            raise ValueError(f"Invalid user_id {user_id}")
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM cooked_history WHERE user_id = ? AND recipe_id = ?",
                            (user_id, recipe_id))
                return cur.fetchone()[0]
        except sqlite3.Error as e:
            logger.error(f"Error getting cooked count for user_id {user_id}, recipe_id {recipe_id}: {e}")
            raise