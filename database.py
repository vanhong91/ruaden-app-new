### dùng bcrypt và PostgreSQL 

import logging
import re
import bcrypt
import psycopg2
from psycopg2 import pool, errors
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager
from config import DB_URL
from utils import validate_unit
from localization import get_text

# ========================
# Logging setup
# ========================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():  # Prevent duplicate handlers
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

# ========================
# Connection pool
# ========================
try:
    DB_POOL = psycopg2.pool.ThreadedConnectionPool(minconn=1, maxconn=10, dsn=DB_URL)
except psycopg2.Error as e:
    logger.error(f"Failed to initialize connection pool: {e}")
    raise

# ========================
# Global flag for DB initialization
# ========================
_DB_INITIALIZED = False

# ========================
# Helper functions
# ========================
def normalize_name(name: str) -> str:
    """Normalize inventory/recipe names for comparison by stripping and lowercasing."""
    return name.strip().lower() if isinstance(name, str) else ""

def parse_quantity(quantity: Any) -> Optional[float]:
    """Parse quantity input (supports Vietnamese decimal format like '100,00')."""
    if isinstance(quantity, (int, float)):
        return float(quantity)
    if isinstance(quantity, str):
        try:
            # Replace comma with dot for Vietnamese decimal format
            cleaned = quantity.replace(',', '.').strip()
            return float(cleaned)
        except ValueError:
            logger.error(f"parse_quantity: Invalid quantity format: {quantity}")
            return None
    return None

# ========================
# Database Manager
# ========================
class DatabaseManager:
    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize inventory/recipe names (alias for backward compatibility)."""
        return normalize_name(name)

    # ------------------------
    # Schema validation
    # ------------------------
    @staticmethod
    def check_schema() -> bool:
        """Check if the database schema includes required columns."""
        try:
            with DatabaseManager.get_db_cursor() as cur:
                cur.execute("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'users' AND column_name = 'password';
                """)
                if not cur.fetchone():
                    logger.error("check_schema: Column 'password' does not exist in 'users' table")
                    return False
                return True
        except psycopg2.Error as e:
            logger.error(f"check_schema: Database error: {e}")
            return False

    # ------------------------
    # Context managers
    # ------------------------
    @staticmethod
    @contextmanager
    def get_db_conn():
        """Provide a database connection from the pool with commit/rollback handling."""
        conn = None
        try:
            conn = DB_POOL.getconn()
            yield conn
            conn.commit()
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                DB_POOL.putconn(conn)

    @staticmethod
    @contextmanager
    def get_db_cursor():
        """Provide a cursor from a connection with auto-close."""
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            try:
                yield cur
            finally:
                cur.close()

    # ------------------------
    # Validation
    # ------------------------
    @staticmethod
    def validate_name(name: Optional[str]) -> bool:
        """Validate an ingredient or recipe name (supports Unicode letters, numbers, space, hyphen, underscore, single quote)."""
        normalized = DatabaseManager.normalize_name(name)
        if not normalized:
            return False
        # Allow Unicode letters, numbers, space, hyphen, underscore, single quote
        return bool(re.match(r'^[\w\s\-\']+$', normalized, re.UNICODE))

    @staticmethod
    def validate_password(password: Optional[str]) -> bool:
        """Validate password: min 8 chars, at least one letter and one digit."""
        if not isinstance(password, str) or not password.strip():
            return False
        return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$", password.strip()))

    @staticmethod
    def validate_user_id(user_id: Optional[int]) -> bool:
        """Validate if a user_id exists in the users table."""
        if not isinstance(user_id, int) or user_id <= 0:
            return False
        try:
            with DatabaseManager.get_db_cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE id = %s;", (user_id,))
                return cur.fetchone() is not None
        except psycopg2.Error as e:
            logger.error(f"validate_user_id: Database error for user_id={user_id}: {e}")
            return False

    # ------------------------
    # Database initialization
    # ------------------------
    @staticmethod
    def init_db():
        """Initialize database schema and apply migrations if not already done."""
        global _DB_INITIALIZED
        if _DB_INITIALIZED:
            logger.debug("init_db: Database already initialized")
            return
        try:
            with DatabaseManager.get_db_conn() as conn:
                with conn.cursor() as cur:
                    # Create users table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(255) UNIQUE NOT NULL,
                            password BYTEA NOT NULL,
                            security_question TEXT NOT NULL,
                            security_answer TEXT NOT NULL
                        );
                    """)
                    # Apply migration: Ensure password column exists
                    cur.execute("""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = 'users' AND column_name = 'password';
                    """)
                    if not cur.fetchone():
                        cur.execute("""
                            ALTER TABLE users
                            ADD COLUMN password BYTEA NOT NULL DEFAULT '\\x00';
                        """)
                    # Create other tables
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS inventory (
                            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                            name VARCHAR(255) NOT NULL,
                            quantity FLOAT NOT NULL,
                            unit VARCHAR(50) NOT NULL,
                            PRIMARY KEY (user_id, name, unit)
                        );
                    """)
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS recipes (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                            title VARCHAR(255) NOT NULL,
                            category VARCHAR(255),
                            instructions TEXT,
                            servings FLOAT NOT NULL,
                            is_signature BOOLEAN NOT NULL DEFAULT FALSE,
                            UNIQUE (user_id, title)
                        );
                    """)
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS recipe_ingredients (
                            recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
                            name VARCHAR(255) NOT NULL,
                            quantity FLOAT NOT NULL,
                            unit VARCHAR(50) NOT NULL,
                            is_spice BOOLEAN NOT NULL DEFAULT FALSE,
                            PRIMARY KEY (recipe_id, name, unit)
                        );
                    """)
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS cooked_history (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                            recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
                            cooked_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
            _DB_INITIALIZED = True
            logger.info("init_db: Database schema initialized successfully")
        except psycopg2.Error as e:
            logger.error(f"init_db: Failed to initialize database: {e}")
            raise

    # ------------------------
    # User management
    # ------------------------
    @staticmethod
    def create_user(username: str, password: str, sec_question: str, sec_answer: str) -> Tuple[bool, str]:
        """Create a new user with a hashed password and security question."""
        if not DatabaseManager.check_schema():
            return False, get_text("db_error").format(error="Cột 'password' không tồn tại trong bảng users")
        username = normalize_name(username)
        if not username:
            logger.error("create_user: Empty or invalid username")
            return False, get_text("invalid_name")
        if not DatabaseManager.validate_password(password):
            logger.error("create_user: Invalid password format for username '%s'", username)
            return False, "Mật khẩu phải có ít nhất 8 ký tự, bao gồm ít nhất một chữ cái và một số."
        if not sec_question.strip() or not sec_answer.strip():
            logger.error("create_user: Empty security question or answer for username '%s'", username)
            return False, "Câu hỏi và câu trả lời bảo mật là bắt buộc."
        try:
            with DatabaseManager.get_db_cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
                if cur.fetchone():
                    logger.warning("create_user: Username '%s' already exists", username)
                    return False, get_text("username_exists")
                password_bytes = password.strip().encode("utf-8")
                hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
                if isinstance(hashed_password, memoryview):
                    hashed_password = bytes(hashed_password)
                cur.execute(
                    """
                    INSERT INTO users (username, password, security_question, security_answer)
                    VALUES (%s, %s, %s, %s) RETURNING id;
                    """,
                    (username, hashed_password, sec_question.strip(), sec_answer.strip())
                )
                user_id = cur.fetchone()[0]
                logger.info("create_user: Successfully created user '%s' with id=%s", username, user_id)
                return True, f"Người dùng '{username}' được tạo thành công"
        except psycopg2.Error as e:
            logger.error("create_user: Database error for username '%s': %s", username, e)
            return False, get_text("db_error").format(error=str(e))
        except Exception as e:
            logger.error("create_user: Unexpected error for username '%s': %s", username, e)
            return False, get_text("db_error").format(error=str(e))

    @staticmethod
    def verify_login(username: str, password: str) -> Optional[int]:
        """Verify user login and return user_id if successful."""
        if not DatabaseManager.check_schema():
            logger.error("verify_login: Database schema error: 'password' column missing")
            return None
        username = normalize_name(username)
        if not username or not password:
            logger.warning("verify_login: Empty username or password")
            return None
        try:
            with DatabaseManager.get_db_cursor() as cur:
                cur.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
                result = cur.fetchone()
                if result:
                    user_id, hashed = result
                    if isinstance(hashed, memoryview):
                        hashed = bytes(hashed)
                    if bcrypt.checkpw(password.strip().encode("utf-8"), hashed):
                        logger.info("verify_login: Successful login for user '%s' (id=%s)", username, user_id)
                        return user_id
                logger.warning("verify_login: Failed login attempt for username '%s'", username)
                return None
        except psycopg2.Error as e:
            logger.error(f"verify_login: Database error for username '{username}': {e}")
            return None

    @staticmethod
    def reset_password(username: str, sec_answer: str, new_password: str) -> bool:
        """Reset user password if security answer matches."""
        if not DatabaseManager.check_schema():
            logger.error("reset_password: Database schema error: 'password' column missing")
            return False
        username = normalize_name(username)
        if not username or not DatabaseManager.validate_password(new_password):
            logger.error("reset_password: Invalid username or new password for '%s'", username)
            return False
        try:
            with DatabaseManager.get_db_cursor() as cur:
                cur.execute("SELECT security_answer FROM users WHERE username = %s;", (username,))
                result = cur.fetchone()
                if not result or result[0] != sec_answer.strip():
                    logger.warning("reset_password: Invalid security answer for username '%s'", username)
                    return False
                hashed_password = bcrypt.hashpw(new_password.strip().encode("utf-8"), bcrypt.gensalt())
                if isinstance(hashed_password, memoryview):
                    hashed_password = bytes(hashed_password)
                cur.execute(
                    "UPDATE users SET password = %s WHERE username = %s;",
                    (hashed_password, username)
                )
                logger.info("reset_password: Password reset successful for username '%s'", username)
                return True
        except psycopg2.Error as e:
            logger.error(f"reset_password: Database error for username '{username}': {e}")
            return False

    # ------------------------
    # Inventory management
    # ------------------------
    @staticmethod
    def list_inventory(user_id: Optional[int]) -> List[Dict]:
        """List all inventory items for a user."""
        if not DatabaseManager.validate_user_id(user_id):
            logger.error("list_inventory: Invalid user_id: %s", user_id)
            return []
        try:
            with DatabaseManager.get_db_cursor() as cur:
                cur.execute(
                    "SELECT name, quantity, unit FROM inventory WHERE user_id = %s ORDER BY name, unit;",
                    (user_id,)
                )
                result = [{"name": row[0], "quantity": row[1], "unit": row[2]} for row in cur.fetchall()]
                logger.debug("list_inventory: Retrieved %d items for user_id=%s", len(result), user_id)
                return result
        except psycopg2.Error as e:
            logger.error(f"list_inventory: Database error for user_id={user_id}: {e}")
            return []

    @staticmethod
    def add_to_inventory(user_id: Optional[int], name: str, quantity: Any, unit: str) -> Tuple[bool, str]:
        """Add or update an inventory item, returns success status and message."""
        name = normalize_name(name)
        if not DatabaseManager.validate_user_id(user_id):
            logger.error("add_to_inventory: Invalid user_id=%s", user_id)
            return False, get_text("db_error").format(error="ID người dùng không hợp lệ")
        if not DatabaseManager.validate_name(name):
            logger.error("add_to_inventory: Invalid name='%s' for user_id=%s", name, user_id)
            return False, get_text("invalid_name")
        parsed_quantity = parse_quantity(quantity)
        if parsed_quantity is None or parsed_quantity <= 0:
            logger.error("add_to_inventory: Invalid quantity=%s for user_id=%s, name='%s'", quantity, user_id, name)
            return False, "Số lượng phải là một số dương hợp lệ (ví dụ: 100 hoặc 100,00)."
        if not validate_unit(unit):
            logger.error("add_to_inventory: Invalid unit='%s' for user_id=%s, name='%s'", unit, user_id, name)
            return False, "Đơn vị không hợp lệ. Sử dụng g, kg, ml, l, tsp, tbsp, cup, piece, cái, pcs, lạng, chén, bát."
        try:
            with DatabaseManager.get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO inventory (user_id, name, quantity, unit)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (user_id, name, unit)
                        DO UPDATE SET quantity = inventory.quantity + EXCLUDED.quantity;
                        """,
                        (user_id, name, parsed_quantity, unit)
                    )
                logger.info("add_to_inventory: Added/updated %s %s %s for user_id=%s", parsed_quantity, unit, name, user_id)
                return True, f"Đã thêm/cập nhật {parsed_quantity} {unit} {name} vào kho"
        except psycopg2.Error as e:
            logger.error(f"add_to_inventory: Database error for user_id={user_id}, name='{name}': {e}")
            return False, get_text("db_error").format(error=str(e))

    @staticmethod
    def consume_base(user_id: Optional[int], name: str, quantity: Any, base_unit: str, conn: Any = None) -> bool:
        """Consume a quantity of an ingredient in base units."""
        name = normalize_name(name)
        if not DatabaseManager.validate_user_id(user_id) or not DatabaseManager.validate_name(name):
            logger.error("consume_base: Invalid user_id=%s or name='%s'", user_id, name)
            return False
        parsed_quantity = parse_quantity(quantity)
        if parsed_quantity is None or parsed_quantity <= 0 or not validate_unit(base_unit):
            logger.error("consume_base: Invalid quantity=%s or base_unit='%s' for user_id=%s", quantity, base_unit, user_id)
            return False
        try:
            close_conn = False
            if conn is None:
                conn = DB_POOL.getconn()
                close_conn = True
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT quantity, unit FROM inventory
                    WHERE user_id = %s AND name = %s AND unit = %s;
                    """,
                    (user_id, name, base_unit)
                )
                result = cur.fetchone()
                if not result:
                    logger.error("consume_base: Ingredient '%s' (%s) not found for user_id=%s", name, base_unit, user_id)
                    if close_conn:
                        conn.rollback()
                        DB_POOL.putconn(conn)
                    return False
                available_qty = result[0]
                if available_qty < parsed_quantity - 1e-6:
                    logger.error("consume_base: Insufficient quantity for '%s': need %s %s, have %s %s", name, parsed_quantity, base_unit, available_qty, base_unit)
                    if close_conn:
                        conn.rollback()
                        DB_POOL.putconn(conn)
                    return False
                new_qty = available_qty - parsed_quantity
                if new_qty <= 1e-6:
                    cur.execute(
                        "DELETE FROM inventory WHERE user_id = %s AND name = %s AND unit = %s;",
                        (user_id, name, base_unit)
                    )
                else:
                    cur.execute(
                        "UPDATE inventory SET quantity = %s WHERE user_id = %s AND name = %s AND unit = %s;",
                        (new_qty, user_id, name, base_unit)
                    )
                logger.info("consume_base: Consumed %s %s of '%s' for user_id=%s, remaining=%s", parsed_quantity, base_unit, name, user_id, new_qty)
            if close_conn:
                conn.commit()
                DB_POOL.putconn(conn)
            return True
        except psycopg2.Error as e:
            logger.error(f"consume_base: Database error for user_id={user_id}, name='{name}': {e}")
            if close_conn:
                conn.rollback()
                DB_POOL.putconn(conn)
            return False

    @staticmethod
    def remove_inventory_item(user_id: Optional[int], name: str, unit: str) -> None:
        """Remove an inventory item."""
        name = normalize_name(name)
        if not DatabaseManager.validate_user_id(user_id) or not DatabaseManager.validate_name(name):
            logger.error("remove_inventory_item: Invalid user_id=%s or name='%s'", user_id, name)
            return
        try:
            with DatabaseManager.get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM inventory WHERE user_id = %s AND name = %s AND unit = %s;",
                        (user_id, name, unit)
                    )
                logger.info("remove_inventory_item: Removed %s (%s) for user_id=%s", name, unit, user_id)
        except psycopg2.Error as e:
            logger.error(f"remove_inventory_item: Database error for user_id={user_id}, name='{name}': {e}")

    # ------------------------
    # Recipe management
    # ------------------------
    @staticmethod
    def list_recipes(user_id: Optional[int]) -> List[Dict]:
        """List all recipes for a user with their ingredients."""
        if not DatabaseManager.validate_user_id(user_id):
            logger.error("list_recipes: Invalid user_id: %s", user_id)
            return []
        try:
            with DatabaseManager.get_db_cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, category, instructions, servings, is_signature
                    FROM recipes WHERE user_id = %s ORDER BY title;
                    """,
                    (user_id,)
                )
                recipes = [
                    {
                        "id": row[0],
                        "title": row[1],
                        "category": row[2],
                        "instructions": row[3],
                        "servings": row[4],
                        "is_signature": row[5],
                        "ingredients": []
                    } for row in cur.fetchall()
                ]
                for recipe in recipes:
                    cur.execute(
                        """
                        SELECT name, quantity, unit, is_spice
                        FROM recipe_ingredients
                        WHERE recipe_id = %s ORDER BY name, unit;
                        """,
                        (recipe["id"],)
                    )
                    recipe["ingredients"] = [
                        {"name": row[0], "quantity": row[1], "unit": row[2], "is_spice": row[3]}
                        for row in cur.fetchall()
                    ]
                logger.debug("list_recipes: Retrieved %d recipes for user_id=%s", len(recipes), user_id)
                return recipes
        except psycopg2.Error as e:
            logger.error(f"list_recipes: Database error for user_id={user_id}: {e}")
            return []

    @staticmethod
    def add_recipe(user_id: Optional[int], recipe: Dict) -> Tuple[bool, str]:
        """Add a new recipe with ingredients."""
        if not DatabaseManager.validate_user_id(user_id):
            logger.error("add_recipe: Invalid user_id: %s", user_id)
            return False, get_text("db_error").format(error="ID người dùng không hợp lệ")
        title = normalize_name(recipe.get("title", ""))
        if not title or not DatabaseManager.validate_name(title):
            logger.error("add_recipe: Invalid recipe title: '%s'", title)
            return False, get_text("error_title_required")
        ingredients = recipe.get("ingredients", [])
        for ing in ingredients:
            ing["quantity"] = parse_quantity(ing.get("quantity", 0))
        if not ingredients or not all(
            DatabaseManager.validate_name(ing.get("name", "")) and
            isinstance(ing.get("quantity", 0), (int, float)) and ing.get("quantity", 0) > 0 and
            validate_unit(ing.get("unit", ""))
            for ing in ingredients
        ):
            logger.error("add_recipe: Invalid ingredients for recipe '%s'", title)
            return False, get_text("error_ingredients_required")
        try:
            with DatabaseManager.get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO recipes (user_id, title, category, instructions, servings, is_signature)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                        """,
                        (
                            user_id,
                            title,
                            recipe.get("category", ""),
                            recipe.get("instructions", ""),
                            parse_quantity(recipe.get("servings", 1.0)),
                            recipe.get("is_signature", False)
                        )
                    )
                    recipe_id = cur.fetchone()[0]
                    for ing in ingredients:
                        cur.execute(
                            """
                            INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit, is_spice)
                            VALUES (%s, %s, %s, %s, %s);
                            """,
                            (
                                recipe_id,
                                normalize_name(ing["name"]),
                                ing["quantity"],
                                ing["unit"],
                                ing.get("is_spice", False)
                            )
                        )
                logger.info("add_recipe: Successfully added recipe '%s' (id=%s) for user_id=%s", title, recipe_id, user_id)
                return True, f"Công thức '{title}' được thêm thành công"
        except psycopg2.Error as e:
            if isinstance(e, errors.UniqueViolation):
                logger.warning("add_recipe: Recipe '%s' already exists for user_id=%s", title, user_id)
                return False, get_text("duplicate_recipe")
            logger.error(f"add_recipe: Database error for user_id={user_id}, title='{title}': {e}")
            return False, get_text("db_error").format(error=str(e))

    @staticmethod
    def update_recipe(user_id: Optional[int], recipe_id: int, recipe: Dict) -> Tuple[bool, str]:
        """Update an existing recipe and its ingredients."""
        if not DatabaseManager.validate_user_id(user_id):
            logger.error("update_recipe: Invalid user_id: %s", user_id)
            return False, get_text("db_error").format(error="ID người dùng không hợp lệ")
        title = normalize_name(recipe.get("title", ""))
        if not title or not DatabaseManager.validate_name(title):
            logger.error("update_recipe: Invalid recipe title: '%s'", title)
            return False, get_text("error_title_required")
        ingredients = recipe.get("ingredients", [])
        for ing in ingredients:
            ing["quantity"] = parse_quantity(ing.get("quantity", 0))
        if not ingredients or not all(
            DatabaseManager.validate_name(ing.get("name", "")) and
            isinstance(ing.get("quantity", 0), (int, float)) and ing.get("quantity", 0) > 0 and
            validate_unit(ing.get("unit", ""))
            for ing in ingredients
        ):
            logger.error("update_recipe: Invalid ingredients for recipe '%s'", title)
            return False, get_text("error_ingredients_required")
        try:
            with DatabaseManager.get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT 1 FROM recipes WHERE id = %s AND user_id = %s;",
                        (recipe_id, user_id)
                    )
                    if not cur.fetchone():
                        logger.error("update_recipe: Recipe id=%s not found for user_id=%s", recipe_id, user_id)
                        return False, "Không tìm thấy công thức"
                    cur.execute(
                        """
                        UPDATE recipes
                        SET title = %s, category = %s, instructions = %s, servings = %s, is_signature = %s
                        WHERE id = %s AND user_id = %s;
                        """,
                        (
                            title,
                            recipe.get("category", ""),
                            recipe.get("instructions", ""),
                            parse_quantity(recipe.get("servings", 1.0)),
                            recipe.get("is_signature", False),
                            recipe_id,
                            user_id
                        )
                    )
                    cur.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s;", (recipe_id,))
                    for ing in ingredients:
                        cur.execute(
                            """
                            INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit, is_spice)
                            VALUES (%s, %s, %s, %s, %s);
                            """,
                            (
                                recipe_id,
                                normalize_name(ing["name"]),
                                ing["quantity"],
                                ing["unit"],
                                ing.get("is_spice", False)
                            )
                        )
                logger.info("update_recipe: Successfully updated recipe '%s' (id=%s) for user_id=%s", title, recipe_id, user_id)
                return True, f"Công thức '{title}' được cập nhật thành công"
        except psycopg2.Error as e:
            if isinstance(e, errors.UniqueViolation):
                logger.warning("update_recipe: Recipe '%s' already exists for user_id=%s", title, user_id)
                return False, get_text("duplicate_recipe")
            logger.error(f"update_recipe: Database error for user_id={user_id}, recipe_id={recipe_id}: {e}")
            return False, get_text("db_error").format(error=str(e))

    @staticmethod
    def delete_recipe(user_id: Optional[int], recipe_id: int) -> Tuple[bool, str]:
        """Delete a recipe and its ingredients."""
        if not DatabaseManager.validate_user_id(user_id):
            logger.error("delete_recipe: Invalid user_id: %s", user_id)
            return False, get_text("db_error").format(error="ID người dùng không hợp lệ")
        try:
            with DatabaseManager.get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT title FROM recipes WHERE id = %s AND user_id = %s;",
                        (recipe_id, user_id)
                    )
                    result = cur.fetchone()
                    if not result:
                        logger.error("delete_recipe: Recipe id=%s not found for user_id=%s", recipe_id, user_id)
                        return False, "Không tìm thấy công thức"
                    title = result[0]
                    cur.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s;", (recipe_id,))
                    cur.execute("DELETE FROM recipes WHERE id = %s AND user_id = %s;", (recipe_id, user_id))
                logger.info("delete_recipe: Successfully deleted recipe '%s' (id=%s) for user_id=%s", title, recipe_id, user_id)
                return True, f"Công thức '{title}' đã được xóa thành công"
        except psycopg2.Error as e:
            logger.error(f"delete_recipe: Database error for user_id={user_id}, recipe_id={recipe_id}: {e}")
            return False, get_text("db_error").format(error=str(e))

    # ------------------------
    # Cooking history
    # ------------------------
    @staticmethod
    def log_cooked_recipe(user_id: Optional[int], recipe_id: int) -> None:
        """Log a recipe as cooked."""
        if not DatabaseManager.validate_user_id(user_id):
            logger.error("log_cooked_recipe: Invalid user_id: %s", user_id)
            return
        try:
            with DatabaseManager.get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT 1 FROM recipes WHERE id = %s AND user_id = %s;",
                        (recipe_id, user_id)
                    )
                    if not cur.fetchone():
                        logger.error("log_cooked_recipe: Recipe id=%s not found for user_id=%s", recipe_id, user_id)
                        return
                    cur.execute(
                        """
                        INSERT INTO cooked_history (user_id, recipe_id, cooked_date)
                        VALUES (%s, %s, CURRENT_TIMESTAMP);
                        """,
                        (user_id, recipe_id)
                    )
                logger.info("log_cooked_recipe: Logged recipe id=%s for user_id=%s", recipe_id, user_id)
        except psycopg2.Error as e:
            logger.error(f"log_cooked_recipe: Database error for user_id={user_id}, recipe_id={recipe_id}: {e}")

    @staticmethod
    def list_cooked_history(user_id: Optional[int]) -> List[Dict]:
        """List cooking history for a user."""
        if not DatabaseManager.validate_user_id(user_id):
            logger.error("list_cooked_history: Invalid user_id: %s", user_id)
            return []
        try:
            with DatabaseManager.get_db_cursor() as cur:
                cur.execute(
                    """
                    SELECT ch.recipe_id, ch.cooked_date
                    FROM cooked_history ch
                    JOIN recipes r ON ch.recipe_id = r.id
                    WHERE ch.user_id = %s
                    ORDER BY ch.cooked_date DESC;
                    """,
                    (user_id,)
                )
                result = [
                    {"recipe_id": row[0], "cooked_date": row[1].strftime("%Y-%m-%d %H:%M:%S")}
                    for row in cur.fetchall()
                ]
                logger.debug("list_cooked_history: Retrieved %d history entries for user_id=%s", len(result), user_id)
                return result
        except psycopg2.Error as e:
            logger.error(f"list_cooked_history: Database error for user_id={user_id}: {e}")
            return []