# import sqlite3
# from typing import Optional, List, Dict, Any
# from config import DB_NAME
# import logging
# from utils import validate_unit

# logger = logging.getLogger(__name__)


# class DatabaseManager:
#     @staticmethod
#     def get_db_conn():
#         """Get a database connection with row factory."""
#         conn = sqlite3.connect(DB_NAME)
#         conn.row_factory = sqlite3.Row
#         return conn

#     @staticmethod
#     def normalize_name(name: str) -> str:
#         """Normalize inventory/recipe names for comparison."""
#         return name.strip().lower() if isinstance(name, str) else ""

#     @staticmethod
#     def validate_name(name: Optional[str]) -> bool:
#         """Validate an ingredient or recipe name."""
#         normalized = DatabaseManager.normalize_name(name)
#         if not normalized:
#             return False
#         return bool(all(c.isalnum() or c.isspace() or c in "-_'()" for c in normalized))

#     @staticmethod
#     def validate_user_id(user_id: int) -> bool:
#         """Validate if a user_id exists in the users table."""
#         with DatabaseManager.get_db_conn() as conn:
#             cur = conn.cursor()
#             cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
#             return cur.fetchone() is not None

#     @staticmethod
#     def init_db():
#         """Initialize the database schema."""
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 # Users table
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS users (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         username TEXT UNIQUE NOT NULL,
#                         password TEXT NOT NULL,
#                         security_question TEXT NOT NULL,
#                         security_answer TEXT NOT NULL
#                     )
#                 """)
#                 # Recipes table
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS recipes (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         user_id INTEGER,
#                         title TEXT NOT NULL,
#                         category TEXT,
#                         instructions TEXT,
#                         servings REAL NOT NULL DEFAULT 1.0,
#                         is_signature INTEGER DEFAULT 0,
#                         FOREIGN KEY (user_id) REFERENCES users(id)
#                     )
#                 """)
#                 # Ingredients table
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS ingredients (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         recipe_id INTEGER,
#                         name TEXT NOT NULL,
#                         quantity REAL NOT NULL,
#                         unit TEXT NOT NULL,
#                         is_spice BOOLEAN NOT NULL,
#                         FOREIGN KEY (recipe_id) REFERENCES recipes(id)
#                     )
#                 """)
#                 # Inventory table
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS inventory (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         user_id INTEGER,
#                         name TEXT NOT NULL,
#                         quantity REAL NOT NULL,
#                         unit TEXT NOT NULL,
#                         FOREIGN KEY (user_id) REFERENCES users(id)
#                     )
#                 """)
#                 # Adjusted recipes
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS adjusted_recipes (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         user_id INTEGER,
#                         title TEXT NOT NULL,
#                         category TEXT,
#                         instructions TEXT,
#                         servings REAL NOT NULL DEFAULT 1.0,
#                         origin_id INTEGER,
#                         FOREIGN KEY (user_id) REFERENCES users(id),
#                         FOREIGN KEY (origin_id) REFERENCES recipes(id)
#                     )
#                 """)
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS adjusted_ingredients (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         adjusted_recipe_id INTEGER,
#                         name TEXT NOT NULL,
#                         quantity REAL NOT NULL,
#                         unit TEXT NOT NULL,
#                         is_spice BOOLEAN NOT NULL,
#                         FOREIGN KEY (adjusted_recipe_id) REFERENCES adjusted_recipes(id)
#                     )
#                 """)
#                 # Cooked history
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS cooked_history (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         user_id INTEGER,
#                         recipe_id INTEGER,
#                         cooked_date DATETIME DEFAULT CURRENT_TIMESTAMP,
#                         FOREIGN KEY (user_id) REFERENCES users(id),
#                         FOREIGN KEY (recipe_id) REFERENCES recipes(id)
#                     )
#                 """)
#                 # Add is_signature if not exists
#                 try:
#                     cur.execute("ALTER TABLE recipes ADD COLUMN is_signature INTEGER DEFAULT 0")
#                 except sqlite3.OperationalError as e:
#                     if "duplicate column name" not in str(e).lower():
#                         logger.warning(f"Could not add is_signature column: {e}")
#                 conn.commit()
#                 logger.info("Database schema initialized successfully")
#         except sqlite3.Error as e:
#             logger.error(f"Error initializing database schema: {e}")
#             raise

#     # ---------------- User Methods ----------------
#     @staticmethod
#     def verify_login(username: str, password: str) -> Optional[int]:
#         with DatabaseManager.get_db_conn() as conn:
#             cur = conn.cursor()
#             cur.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#             result = cur.fetchone()
#             return result[0] if result else None

#     @staticmethod
#     def create_user(username: str, password: str, security_question: str, security_answer: str) -> tuple[bool, str]:
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 cur.execute("INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)",
#                             (username, password, security_question, security_answer))
#                 conn.commit()
#                 return True, "User created successfully."
#         except sqlite3.IntegrityError:
#             return False, "Username already exists."

#     @staticmethod
#     def reset_password(username: str, security_answer: str, new_password: str) -> bool:
#         with DatabaseManager.get_db_conn() as conn:
#             cur = conn.cursor()
#             cur.execute("SELECT id FROM users WHERE username = ? AND security_answer = ?", (username, security_answer))
#             user = cur.fetchone()
#             if user:
#                 cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user[0]))
#                 conn.commit()
#                 return True
#             return False

#     # ---------------- Inventory Methods ----------------
#     @staticmethod
#     def list_inventory(user_id: int) -> List[Dict[str, Any]]:
#         with DatabaseManager.get_db_conn() as conn:
#             cur = conn.cursor()
#             cur.execute("SELECT id, name, quantity, unit FROM inventory WHERE user_id = ?", (user_id,))
#             return [dict(row) for row in cur.fetchall()]

#     @staticmethod
#     def upsert_inventory(user_id: int, name: str, quantity: float, unit: str) -> bool:
#         with DatabaseManager.get_db_conn() as conn:
#             cur = conn.cursor()
#             cur.execute("SELECT id FROM inventory WHERE user_id = ? AND name = ? AND unit = ?", (user_id, name, unit))
#             row = cur.fetchone()
#             if row:
#                 cur.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (quantity, row[0]))
#             else:
#                 cur.execute("INSERT INTO inventory (user_id, name, quantity, unit) VALUES (?, ?, ?, ?)",
#                             (user_id, name, quantity, unit))
#             conn.commit()
#             return True

#     @staticmethod
#     def update_inventory_item(item_id: int, name: str, quantity: float, unit: str) -> bool:
#         with DatabaseManager.get_db_conn() as conn:
#             cur = conn.cursor()
#             cur.execute("UPDATE inventory SET name = ?, quantity = ?, unit = ? WHERE id = ?",
#                         (name, quantity, unit, item_id))
#             conn.commit()
#             return cur.rowcount > 0

#     @staticmethod
#     def delete_inventory(item_id: int) -> bool:
#         with DatabaseManager.get_db_conn() as conn:
#             cur = conn.cursor()
#             cur.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
#             conn.commit()
#             return cur.rowcount > 0

#     @staticmethod
#     def consume_base(user_id: int, name: str, base_qty: float, base_unit: str, conn=None) -> bool:
#         """Consume a specified quantity of an ingredient from inventory."""
#         try:
#             if not conn:
#                 conn = DatabaseManager.get_db_conn()
#                 close_conn = True
#             else:
#                 close_conn = False
#             cur = conn.cursor()
#             cur.execute("SELECT id, quantity, unit FROM inventory WHERE user_id = ? AND name = ? AND unit = ?",
#                         (user_id, name, base_unit))
#             row = cur.fetchone()
#             if row:
#                 new_qty = row["quantity"] - base_qty
#                 if new_qty < 0:
#                     logger.warning(f"Insufficient quantity for {name}: {row['quantity']} {base_unit}, need {base_qty}")
#                     return False
#                 if new_qty == 0:
#                     cur.execute("DELETE FROM inventory WHERE id = ?", (row["id"],))
#                 else:
#                     cur.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (new_qty, row["id"]))
#                 if close_conn:
#                     conn.commit()
#                 return True
#             logger.warning(f"Item {name} ({base_unit}) not found in inventory for user_id {user_id}")
#             return False
#         except sqlite3.Error as e:
#             logger.error(f"Error consuming {name} ({base_qty} {base_unit}) for user_id {user_id}: {e}")
#             return False
#         finally:
#             if close_conn and conn:
#                 conn.close()

#     # ---------------- Recipe Methods ----------------
#     @staticmethod
#     def create_recipe_from_table(user_id: int, title: str, category: str, instructions: str,
#                                  ingredients: List[Dict[str, Any]], recipe_id: Optional[int] = None,
#                                  is_signature: bool = False, servings: float = 1.0) -> tuple[bool, str]:
#         """Create or update a recipe in the database."""
#         if not DatabaseManager.validate_user_id(user_id):
#             return False, f"Invalid user_id {user_id}"
#         normalized_title = DatabaseManager.normalize_name(title)
#         if not normalized_title:
#             return False, "Invalid recipe title"
#         valid_ingredients = []
#         for ing in ingredients:
#             if not all(key in ing for key in ["name", "quantity", "unit"]):
#                 return False, f"Invalid ingredient format: {ing}"
#             if not DatabaseManager.normalize_name(ing["name"]):
#                 continue
#             if not validate_unit(ing["unit"]):
#                 return False, f"Invalid unit: {ing['unit']}"
#             if not isinstance(ing["quantity"], (int, float)) or ing["quantity"] <= 0:
#                 continue
#             valid_ingredients.append(ing)
#         if not valid_ingredients:
#             return False, "No valid ingredients provided"
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 if recipe_id:
#                     cur.execute(
#                         "UPDATE recipes SET title = ?, category = ?, instructions = ?, servings = ?, is_signature = ? WHERE id = ? AND user_id = ?",
#                         (normalized_title, category, instructions, servings, int(is_signature), recipe_id, user_id)
#                     )
#                     if cur.rowcount == 0:
#                         return False, "Recipe not found or not owned by user"
#                     cur.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
#                 else:
#                     cur.execute(
#                         "INSERT INTO recipes (user_id, title, category, instructions, servings, is_signature) VALUES (?, ?, ?, ?, ?, ?)",
#                         (user_id, normalized_title, category, instructions, servings, int(is_signature))
#                     )
#                     recipe_id = cur.lastrowid
#                 for ing in valid_ingredients:
#                     cur.execute(
#                         "INSERT INTO ingredients (recipe_id, name, quantity, unit, is_spice) VALUES (?, ?, ?, ?, ?)",
#                         (recipe_id, DatabaseManager.normalize_name(ing["name"]), ing["quantity"], ing["unit"], ing.get("is_spice", False))
#                     )
#                 conn.commit()
#                 return True, "Recipe saved successfully"
#         except sqlite3.Error as e:
#             return False, f"Database error: {str(e)}"

#     # Alias to fix backward compatibility
#     create_recipe = create_recipe_from_table

#     @staticmethod
#     def get_recipe_by_title(user_id: int, title: str) -> Optional[Dict[str, Any]]:
#         """Get a recipe by title for a user."""
#         if not DatabaseManager.validate_user_id(user_id):
#             return None
#         normalized_title = DatabaseManager.normalize_name(title)
#         if not normalized_title:
#             return None
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 cur.execute(
#                     "SELECT id, title, category, instructions, servings, is_signature FROM recipes WHERE user_id = ? AND title = ?",
#                     (user_id, normalized_title)
#                 )
#                 recipe = cur.fetchone()
#                 if recipe:
#                     recipe_dict = {
#                         "id": recipe["id"],
#                         "title": recipe["title"],
#                         "category": recipe["category"],
#                         "instructions": recipe["instructions"],
#                         "servings": recipe["servings"],
#                         "is_signature": bool(recipe["is_signature"])
#                     }
#                     cur.execute("SELECT name, quantity, unit, is_spice FROM ingredients WHERE recipe_id = ?", (recipe_dict["id"],))
#                     recipe_dict["ingredients"] = [
#                         {"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": bool(ing["is_spice"])}
#                         for ing in cur.fetchall()
#                     ]
#                     return recipe_dict
#                 return None
#         except sqlite3.Error as e:
#             logger.error(f"Database error fetching recipe '{title}' for user_id {user_id}: {e}")
#             return None

#     @staticmethod
#     def list_recipes(user_id: int) -> List[Dict[str, Any]]:
#         """List all recipes for a user."""
#         if not DatabaseManager.validate_user_id(user_id):
#             return []
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 cur.execute("SELECT id, title, category, instructions, servings, is_signature FROM recipes WHERE user_id = ?", (user_id,))
#                 recipes = []
#                 for row in cur.fetchall():
#                     recipe_id = row["id"]
#                     cur.execute("SELECT name, quantity, unit, is_spice FROM ingredients WHERE recipe_id = ?", (recipe_id,))
#                     ingredients = [{"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": bool(ing["is_spice"])}
#                                    for ing in cur.fetchall()]
#                     recipes.append({
#                         "id": recipe_id,
#                         "title": row["title"],
#                         "category": row["category"],
#                         "instructions": row["instructions"],
#                         "servings": row["servings"],
#                         "is_signature": bool(row["is_signature"]),
#                         "ingredients": ingredients
#                     })
#                 return recipes
#         except sqlite3.Error as e:
#             logger.error(f"Database error listing recipes for user_id {user_id}: {e}")
#             return []

#     @staticmethod
#     def delete_recipe(recipe_id: int) -> bool:
#         """Delete a recipe and its associated ingredients."""
#         if not isinstance(recipe_id, int) or recipe_id <= 0:
#             return False
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 cur.execute("SELECT title FROM recipes WHERE id = ?", (recipe_id,))
#                 recipe = cur.fetchone()
#                 if not recipe:
#                     return False
#                 cur.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
#                 cur.execute("DELETE FROM cooked_history WHERE recipe_id = ?", (recipe_id,))
#                 cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
#                 conn.commit()
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Database error deleting recipe_id {recipe_id}: {e}")
#             return False

#     # ---------------- Cooked History Methods ----------------
#     @staticmethod
#     def log_cooked_recipe(user_id: int, recipe_id: int):
#         """Log a recipe as cooked in the cooked_history table."""
#         if not DatabaseManager.validate_user_id(user_id):
#             raise ValueError(f"Invalid user_id {user_id}")
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 cur.execute("INSERT INTO cooked_history (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
#                 conn.commit()
#         except sqlite3.Error as e:
#             logger.error(f"Error logging cooked recipe for user_id {user_id}, recipe_id {recipe_id}: {e}")
#             raise

#     @staticmethod
#     def list_cooked_history(user_id: int) -> List[Dict]:
#         """Retrieve the cooking history for a user."""
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 cur.execute("SELECT id, recipe_id, cooked_date FROM cooked_history WHERE user_id = ? ORDER BY cooked_date DESC",
#                             (user_id,))
#                 return [{"id": row["id"], "recipe_id": row["recipe_id"], "cooked_date": str(row["cooked_date"])}
#                         for row in cur.fetchall()]
#         except sqlite3.Error as e:
#             logger.error(f"Error listing cooked history for user_id {user_id}: {e}")
#             raise

#     @staticmethod
#     def get_cooked_count(user_id: int, recipe_id: int) -> int:
#         """Get the number of times a recipe has been cooked by a user."""
#         try:
#             with DatabaseManager.get_db_conn() as conn:
#                 cur = conn.cursor()
#                 cur.execute("SELECT COUNT(*) FROM cooked_history WHERE user_id = ? AND recipe_id = ?",
#                             (user_id, recipe_id))
#                 return cur.fetchone()[0]
#         except sqlite3.Error as e:
#             logger.error(f"Error getting cooked count for user_id {user_id}, recipe_id {recipe_id}: {e}")
#             raise





import sqlite3
from typing import Optional, List, Dict, Any
from config import DB_NAME
import logging
import bcrypt  # Modified for bcrypt: Thêm import bcrypt

logger = logging.getLogger(__name__)

class DatabaseManager:
    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize inventory/recipe names for comparison."""
        return name.strip().lower() if isinstance(name, str) else ""

    @staticmethod
    def get_db_conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def validate_user_id(user_id: int) -> bool:
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            return cur.fetchone() is not None

    @staticmethod
    def verify_login(username: str, password: str) -> Optional[int]:
        """Verify login by comparing hashed password."""
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            result = cur.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result['password']):
                return result['id']
            return None

    @staticmethod
    def create_user(username: str, password: str, security_question: str, security_answer: str) -> tuple[bool, str]:
        """Create a new user with hashed password."""
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cur.execute(
                    "INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)",
                    (username, hashed_password, security_question, security_answer)
                )
                conn.commit()
                return True, "User created successfully."
        except sqlite3.IntegrityError:
            return False, "Username already exists."

    @staticmethod
    def reset_password(username: str, security_answer: str, new_password: str) -> bool:
        """Reset user password with hashing."""
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username = ? AND security_answer = ?", (username, security_answer))
            user = cur.fetchone()
            if user:
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cur.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_new_password, user['id']))
                conn.commit()
                return True
            return False

    @staticmethod
    def list_inventory(user_id: int) -> List[Dict[str, Any]]:
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, quantity, unit FROM inventory WHERE user_id = ?", (user_id,))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def upsert_inventory(user_id: int, name: str, quantity: float, unit: str) -> bool:
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM inventory WHERE user_id = ? AND name = ? AND unit = ?", (user_id, name, unit))
            row = cur.fetchone()
            if row:
                cur.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (quantity, row['id']))
            else:
                cur.execute("INSERT INTO inventory (user_id, name, quantity, unit) VALUES (?, ?, ?, ?)",
                            (user_id, name, quantity, unit))
            conn.commit()
            return True

    @staticmethod
    def update_inventory_item(item_id: int, name: str, quantity: float, unit: str) -> bool:
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE inventory SET name = ?, quantity = ?, unit = ? WHERE id = ?",
                        (name, quantity, unit, item_id))
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def delete_inventory(item_id: int) -> bool:
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def list_recipes(user_id: int) -> List[Dict[str, Any]]:
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, title, category, instructions, servings, is_signature FROM recipes WHERE user_id = ?", (user_id,))
                recipes = []
                for row in cur.fetchall():
                    recipe_id = row["id"]
                    cur.execute("SELECT name, quantity, unit, is_spice FROM ingredients WHERE recipe_id = ?", (recipe_id,))
                    ingredients = [{"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": bool(ing["is_spice"])}
                                   for ing in cur.fetchall()]
                    recipes.append({
                        "id": recipe_id,
                        "title": row["title"],
                        "category": row["category"],
                        "instructions": row["instructions"],
                        "servings": row["servings"],
                        "is_signature": bool(row["is_signature"]),
                        "ingredients": ingredients
                    })
                return recipes
        except sqlite3.Error as e:
            logger.error(f"Database error listing recipes for user_id {user_id}: {e}")
            return []

    @staticmethod
    def create_recipe_from_table(user_id: int, title: str, category: str, instructions: str, ingredients: List[Dict[str, Any]], servings: int = 1, is_signature: bool = False, recipe_id: Optional[int] = None) -> tuple[bool, str]:
        """Create or update a recipe with associated ingredients."""
        normalized_title = DatabaseManager.normalize_name(title)
        if not normalized_title:
            return False, "Recipe title is required"
        valid_ingredients = [ing for ing in ingredients if ing.get("name") and isinstance(ing.get("quantity"), (int, float)) and ing.get("quantity") > 0]
        if not valid_ingredients:
            return False, "No valid ingredients provided"
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                if recipe_id:
                    cur.execute(
                        "UPDATE recipes SET title = ?, category = ?, instructions = ?, servings = ?, is_signature = ? WHERE id = ? AND user_id = ?",
                        (normalized_title, category, instructions, servings, int(is_signature), recipe_id, user_id)
                    )
                    if cur.rowcount == 0:
                        return False, "Recipe not found or not owned by user"
                    cur.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
                else:
                    cur.execute(
                        "INSERT INTO recipes (user_id, title, category, instructions, servings, is_signature) VALUES (?, ?, ?, ?, ?, ?)",
                        (user_id, normalized_title, category, instructions, servings, int(is_signature))
                    )
                    recipe_id = cur.lastrowid
                for ing in valid_ingredients:
                    cur.execute(
                        "INSERT INTO ingredients (recipe_id, name, quantity, unit, is_spice) VALUES (?, ?, ?, ?, ?)",
                        (recipe_id, DatabaseManager.normalize_name(ing["name"]), ing["quantity"], ing["unit"], ing.get("is_spice", False))
                    )
                conn.commit()
                return True, "Recipe saved successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    create_recipe = create_recipe_from_table

    @staticmethod
    def get_recipe_by_title(user_id: int, title: str) -> Optional[Dict[str, Any]]:
        """Get a recipe by title for a user."""
        if not DatabaseManager.validate_user_id(user_id):
            return None
        normalized_title = DatabaseManager.normalize_name(title)
        if not normalized_title:
            return None
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, title, category, instructions, servings, is_signature FROM recipes WHERE user_id = ? AND title = ?",
                    (user_id, normalized_title)
                )
                recipe = cur.fetchone()
                if recipe:
                    recipe_dict = {
                        "id": recipe["id"],
                        "title": recipe["title"],
                        "category": recipe["category"],
                        "instructions": recipe["instructions"],
                        "servings": recipe["servings"],
                        "is_signature": bool(recipe["is_signature"])
                    }
                    cur.execute("SELECT name, quantity, unit, is_spice FROM ingredients WHERE recipe_id = ?", (recipe_dict["id"],))
                    recipe_dict["ingredients"] = [
                        {"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": bool(ing["is_spice"])}
                        for ing in cur.fetchall()
                    ]
                    return recipe_dict
                return None
        except sqlite3.Error as e:
            logger.error(f"Database error fetching recipe '{title}' for user_id {user_id}: {e}")
            return None

    @staticmethod
    def delete_recipe(recipe_id: int) -> bool:
        """Delete a recipe and its associated ingredients."""
        if not isinstance(recipe_id, int) or recipe_id <= 0:
            return False
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT title FROM recipes WHERE id = ?", (recipe_id,))
                recipe = cur.fetchone()
                if not recipe:
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
        """Log a recipe as cooked in the cooked_history table."""
        if not DatabaseManager.validate_user_id(user_id):
            raise ValueError(f"Invalid user_id {user_id}")
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO cooked_history (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error logging cooked recipe for user_id {user_id}, recipe_id {recipe_id}: {e}")
            raise

    @staticmethod
    def list_cooked_history(user_id: int) -> List[Dict]:
        """Retrieve the cooking history for a user."""
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, recipe_id, cooked_date FROM cooked_history WHERE user_id = ? ORDER BY cooked_date DESC",
                            (user_id,))
                return [{"id": row["id"], "recipe_id": row["recipe_id"], "cooked_date": str(row["cooked_date"])}
                        for row in cur.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error listing cooked history for user_id {user_id}: {e}")
            raise

    @staticmethod
    def get_cooked_count(user_id: int, recipe_id: int) -> int:
        """Get the number of times a recipe has been cooked by a user."""
        try:
            with DatabaseManager.get_db_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM cooked_history WHERE user_id = ? AND recipe_id = ?",
                            (user_id, recipe_id))
                return cur.fetchone()[0]
        except sqlite3.Error as e:
            logger.error(f"Error getting cooked count for user_id {user_id}, recipe_id {recipe_id}: {e}")
            raise