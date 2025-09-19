### dùng bcrypt và PostgreSQL 

import streamlit as st
import html
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple, Any
import logging
from collections import defaultdict, Counter
import re
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# Constants
APP_TITLE_EN = "RuaDen Recipe App"
APP_TITLE_VI = "Ứng dụng Công thức RuaDen"
VALID_UNITS = ["g", "kg", "ml", "l", "tsp", "tbsp", "cup", "piece", "pcs", "lạng", "chén", "bát"]
MAX_QUANTITY = 1000.0  # Maximum quantity for ingredients (in base unit, e.g., grams)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/recipe_app")
POSTGRES_SUPERUSER = os.getenv("POSTGRES_SUPERUSER", "postgres")
POSTGRES_SUPERUSER_PASSWORD = os.getenv("POSTGRES_SUPERUSER_PASSWORD", "postgres")
ROLE_NAME = "recipe_user"
ROLE_PASSWORD = "secure_password_123"
DB_NAME = "recipe_app"

# Multilingual text
TEXT = {
    "English": {
        "app_title": APP_TITLE_EN,
        "login": "🔐 Login",
        "username": "Username",
        "password": "Password",
        "login_button": "Login",
        "register": "🆕 Register",
        "sec_question": "Security Question (for password reset)",
        "sec_answer": "Security Answer",
        "create_account": "Create Account",
        "reset_password": "♻️ Reset Password",
        "new_password": "New Password",
        "reset_button": "Reset Password",
        "logout": "Logout",
        "language": "Language",
        "title": "Title",
        "category": "Category",
        "instructions": "Instructions",
        "servings": "Servings",
        "name": "Name",
        "quantity": "Quantity",
        "unit": "Unit",
        "need": "Need",
        "have": "Have",
        "missing": "Missing",
        "inventory": "📦 Inventory",
        "your_stock": "Your Stock",
        "no_ingredients": "No ingredients yet.",
        "unit_tips": "Unit tips: use g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
        "add_ingredient": "Add New Ingredient",
        "recipes": "📖 Recipes",
        "your_recipes": "Your Recipes",
        "no_recipes": "No recipes yet.",
        "save_recipe": "Save Recipe",
        "update_recipe": "Update Recipe",
        "delete_recipe": "Delete Recipe",
        "feasibility": "✅ Feasibility & Shopping",
        "create_recipes_first": "Create recipes first.",
        "you_can_cook": "Recipe Feasibility and Shopping List",
        "none_yet": "None yet.",
        "all_available": "All ingredients available.",
        "cook": "Cook",
        "missing_something": "Missing Ingredients",
        "all_feasible": "All recipes are feasible 🎉",
        "add_to_shopping": "Add missing to Shopping List",
        "shopping_list": "🛒 Shopping List",
        "empty_list": "Your shopping list is empty.",
        "update_inventory": "Update Inventory from Shopping List",
        "purchased": "Inventory updated with purchased items.",
        "select_recipes_label": "Select recipes to proceed",
        "select_purchased": "Select purchased items",
        "sent_to_shopping": "Missing ingredients added to the shopping list.",
        "cook_success": "Cooked successfully.",
        "cook_failed": "Cooking failed: {error}",
        "adjust_recipe": "⚖️ Adjust Recipe",
        "select_recipe": "Select Recipe",
        "adjustment_type": "Adjustment Type",
        "by_servings": "By Servings",
        "by_main_ingredient": "By Main Ingredient",
        "new_servings": "New Servings",
        "main_ingredient": "Main Ingredient",
        "new_quantity": "New Quantity",
        "spice_level": "Spice Adjustment",
        "mild": "Mild (60%)",
        "normal": "Normal (80%)",
        "rich": "Rich (100%)",
        "adjusted_recipe": "Adjusted Recipe",
        "cook_adjusted": "Cook Adjusted Recipe",
        "add_to_shopping_adjusted": "Add Missing to Shopping List",
        "adjusted_recipe_title": "Adjusted: {title}",
        "no_recipe_selected": "Please select a recipe to adjust.",
        "invalid_adjustment": "Invalid adjustment parameters.",
        "insufficient_ingredients": "Insufficient ingredients to cook the adjusted recipe.",
        "empty_inventory_warning": "Your inventory is empty. Please add ingredients in the Inventory tab to check feasibility.",
        "cook_adjusted_success": "Adjusted recipe '{title}' cooked successfully.",
        "cook_adjusted_failed": "Failed to cook adjusted recipe '{title}': {error}",
        "not_logged_in": "You must be logged in to access this page.",
        "error_title_required": "Recipe title is required.",
        "error_ingredients_required": "At least one valid ingredient (with name and positive quantity) is required.",
        "duplicate_recipe": "A recipe with this title already exists.",
        "error_invalid_name": "Invalid ingredient name: {name}",
        "error_invalid_unit": "Invalid unit: {unit}",
        "error_negative_qty": "Quantity must be positive for ingredient: {name}",
        "error_excessive_qty": "Quantity too large for ingredient: {name} (max {max_qty} {unit})",
        "save_success": "Recipe '{title}' saved successfully.",
        "update_success": "Recipe '{title}' updated successfully.",
        "delete_success": "Recipe '{title}' deleted successfully.",
        "save_failed": "Failed to save recipe '{title}': {error}",
        "update_failed": "Failed to update recipe '{title}': {error}",
        "delete_failed": "Failed to delete recipe '{title}': {error}",
        "food_timeline": "🍲 Food Timeline",
        "no_history": "No cooking history yet.",
        "no_entries": "No entries match the filters.",
        "congrats": "Congratulations! You have reached {stars} with {dish} 🎉",
        "signature_dish": "Signature Dish",
        "search_placeholder": "Search (e.g., tag:signature, week:1, day:2025-09-01)",
        "reset_filter": "🔄 Reset filter",
        "stats_week": "This week you cooked {count} dishes, most frequent: {dish}",
        "db_error": "Database error: {error}",
        "save_changes": "Save Changes",
        "inventory_updated": "Inventory updated successfully.",
        "db_init_failed": "Failed to initialize database: {error}",
        "invalid_quantity": "Invalid quantity format. Use numbers with optional decimal point or comma."
    },
    "Vietnamese": {
        "app_title": APP_TITLE_VI,
        "login": "🔐 Đăng nhập",
        "username": "Tên người dùng",
        "password": "Mật khẩu",
        "login_button": "Đăng nhập",
        "register": "🆕 Đăng ký",
        "sec_question": "Câu hỏi bảo mật (để đặt lại mật khẩu)",
        "sec_answer": "Câu trả lời bảo mật",
        "create_account": "Tạo tài khoản",
        "reset_password": "♻️ Đặt lại mật khẩu",
        "new_password": "Mật khẩu mới",
        "reset_button": "Đặt lại mật khẩu",
        "logout": "Đăng xuất",
        "language": "Ngôn ngữ",
        "title": "Tiêu đề",
        "category": "Danh mục",
        "instructions": "Hướng dẫn",
        "servings": "Khẩu phần",
        "name": "Tên",
        "quantity": "Số lượng",
        "unit": "Đơn vị",
        "need": "Cần",
        "have": "Có",
        "missing": "Thiếu",
        "inventory": "📦 Kho",
        "your_stock": "Kho của bạn",
        "no_ingredients": "Chưa có nguyên liệu.",
        "unit_tips": "Mẹo đơn vị: sử dụng g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
        "add_ingredient": "Thêm nguyên liệu mới",
        "recipes": "📖 Công thức",
        "your_recipes": "Công thức của bạn",
        "no_recipes": "Chưa có công thức.",
        "save_recipe": "Lưu công thức",
        "update_recipe": "Cập nhật công thức",
        "delete_recipe": "Xóa công thức",
        "feasibility": "✅ Tính khả thi & Mua sắm",
        "create_recipes_first": "Vui lòng tạo công thức trước.",
        "you_can_cook": "Tính khả thi công thức và danh sách mua sắm",
        "none_yet": "Chưa có.",
        "all_available": "Tất cả nguyên liệu đều có sẵn.",
        "cook": "Nấu",
        "missing_something": "Thiếu nguyên liệu",
        "all_feasible": "Tất cả công thức đều khả thi 🎉",
        "add_to_shopping": "Thêm nguyên liệu thiếu vào danh sách mua sắm",
        "shopping_list": "🛒 Danh sách mua sắm",
        "empty_list": "Danh sách mua sắm của bạn trống.",
        "update_inventory": "Cập nhật kho từ danh sách mua sắm",
        "purchased": "Kho đã được cập nhật với các mặt hàng đã mua.",
        "select_recipes_label": "Chọn công thức để tiếp tục",
        "select_purchased": "Chọn các mặt hàng đã mua",
        "sent_to_shopping": "Nguyên liệu thiếu đã được thêm vào danh sách mua sắm.",
        "cook_success": "Nấu thành công.",
        "cook_failed": "Nấu thất bại: {error}",
        "adjust_recipe": "⚖️ Điều chỉnh công thức",
        "select_recipe": "Chọn công thức",
        "adjustment_type": "Loại điều chỉnh",
        "by_servings": "Theo khẩu phần",
        "by_main_ingredient": "Theo nguyên liệu chính",
        "new_servings": "Khẩu phần mới",
        "main_ingredient": "Nguyên liệu chính",
        "new_quantity": "Số lượng mới",
        "spice_level": "Điều chỉnh độ cay",
        "mild": "Nhẹ (60%)",
        "normal": "Bình thường (80%)",
        "rich": "Đậm (100%)",
        "adjusted_recipe": "Công thức đã điều chỉnh",
        "cook_adjusted": "Nấu công thức đã điều chỉnh",
        "add_to_shopping_adjusted": "Thêm nguyên liệu thiếu vào danh sách mua sắm",
        "adjusted_recipe_title": "Đã điều chỉnh: {title}",
        "no_recipe_selected": "Vui lòng chọn một công thức để điều chỉnh.",
        "invalid_adjustment": "Tham số điều chỉnh không hợp lệ.",
        "insufficient_ingredients": "Thiếu nguyên liệu để nấu công thức đã điều chỉnh.",
        "empty_inventory_warning": "Kho của bạn đang trống. Vui lòng thêm nguyên liệu ở tab Kho để kiểm tra tính khả thi.",
        "cook_adjusted_success": "Công thức điều chỉnh '{title}' đã nấu thành công.",
        "cook_adjusted_failed": "Không thể nấu công thức điều chỉnh '{title}': {error}",
        "not_logged_in": "Bạn phải đăng nhập để truy cập trang này.",
        "error_title_required": "Tiêu đề công thức là bắt buộc.",
        "error_ingredients_required": "Cần ít nhất một nguyên liệu hợp lệ (với tên và số lượng dương).",
        "duplicate_recipe": "Công thức với tiêu đề này đã tồn tại.",
        "error_invalid_name": "Tên nguyên liệu không hợp lệ: {name}",
        "error_invalid_unit": "Đơn vị không hợp lệ: {unit}",
        "error_negative_qty": "Số lượng phải dương cho nguyên liệu: {name}",
        "error_excessive_qty": "Số lượng quá lớn cho nguyên liệu: {name} (tối đa {max_qty} {unit})",
        "save_success": "Công thức '{title}' đã được lưu thành công.",
        "update_success": "Công thức '{title}' đã được cập nhật thành công.",
        "delete_success": "Công thức '{title}' đã được xóa thành công.",
        "save_failed": "Không thể lưu công thức '{title}': {error}",
        "update_failed": "Không thể cập nhật công thức '{title}': {error}",
        "delete_failed": "Không thể xóa công thức '{title}': {error}",
        "food_timeline": "🍲 Dòng thời gian món ăn",
        "no_history": "Chưa có lịch sử nấu ăn.",
        "no_entries": "Không có mục nào khớp với bộ lọc.",
        "congrats": "Chúc mừng! Bạn đã đạt được {stars} với món {dish} 🎉",
        "signature_dish": "Món tủ",
        "search_placeholder": "Tìm kiếm (ví dụ: tag:signature, week:1, day:2025-09-01)",
        "reset_filter": "🔄 Đặt lại bộ lọc",
        "stats_week": "Tuần này bạn đã nấu {count} món, món thường xuyên nhất: {dish}",
        "db_error": "Lỗi cơ sở dữ liệu: {error}",
        "save_changes": "Lưu thay đổi",
        "inventory_updated": "Kho đã được cập nhật thành công.",
        "db_init_failed": "Không thể khởi tạo cơ sở dữ liệu: {error}",
        "invalid_quantity": "Định dạng số lượng không hợp lệ. Sử dụng số với dấu chấm hoặc dấu phẩy tùy chọn."
    }
}

def get_text(key: str, **kwargs) -> str:
    """Retrieve multilingual text with safe formatting."""
    lang = st.session_state.get("language", "English")
    template = TEXT.get(lang, TEXT["English"]).get(key, key)
    try:
        return template.format(**kwargs)
    except Exception as e:
        logger.warning(f"i18n fallback for key='{key}': {e}")
        return template

# Database initialization
def initialize_database() -> bool:
    """Initialize PostgreSQL database and role if they don't exist."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=POSTGRES_SUPERUSER,
            password=POSTGRES_SUPERUSER_PASSWORD,
            host="localhost",
            port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (ROLE_NAME,))
            if not cursor.fetchone():
                cursor.execute(f"CREATE ROLE {ROLE_NAME} WITH LOGIN PASSWORD %s", (ROLE_PASSWORD,))
                logger.info(f"Created PostgreSQL role: {ROLE_NAME}")
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {DB_NAME}")
                cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {ROLE_NAME}")
                logger.info(f"Created PostgreSQL database: {DB_NAME}")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False

# Database setup
try:
    if not initialize_database():
        st.error(get_text("db_init_failed").format(error="Could not initialize database. Check logs for details."))
        st.stop()
    engine = create_engine(DATABASE_URL, echo=False)
    Base = declarative_base()
    Session = scoped_session(sessionmaker(bind=engine))
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    st.error(get_text("db_error").format(error=str(e)))
    st.stop()

# Database Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    sec_question = Column(String(255), nullable=False)
    sec_answer_hash = Column(String(128), nullable=False)
    inventory = relationship("Inventory", back_populates="user")
    recipes = relationship("Recipe", back_populates="user")
    cooked_history = relationship("CookedHistory", back_populates="user")

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    user = relationship("User", back_populates="inventory")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(255))
    instructions = Column(Text)
    servings = Column(Float, default=1.0)
    is_signature = Column(Boolean, default=False)
    user = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    cooked_history = relationship("CookedHistory", back_populates="recipe", cascade="all, delete-orphan")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    is_spice = Column(Boolean, default=False)
    recipe = relationship("Recipe", back_populates="ingredients")

class CookedHistory(Base):
    __tablename__ = "cooked_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    cooked_date = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="cooked_history")
    recipe = relationship("Recipe", back_populates="cooked_history")

try:
    Base.metadata.create_all(engine)
except Exception as e:
    logger.error(f"Failed to create tables: {e}")
    st.error(get_text("db_error").format(error=str(e)))
    st.stop()

# Export list
__all__ = [
    'inject_css', 'get_text', 'current_user_id', 'initialize_session_state',
    'topbar_account', 'inventory_page', 'recipes_page', 'feasibility_page',
    'shopping_list_page', 'recipe_adjustment_page', 'food_timeline_page',
    'auth_gate_tabs', 'main'
]

def inject_css() -> None:
    """Inject custom CSS for Streamlit app styling."""
    try:
        st.markdown(
            """
            <style>
                .block-container {
                    padding-top: 5rem;
                    padding-bottom: 2rem;
                    max-width: 980px;
                }
                .stTextInput > div > div > input,
                .stNumberInput > div > div > input,
                textarea {
                    border-radius: 12px !important;
                    border: 1px solid #e6e6e6 !important;
                    padding: .55rem .8rem !important;
                }
                .stButton > button {
                    background: #111 !important;
                    color: #fff !important;
                    border: none !important;
                    border-radius: 14px !important;
                    padding: .55rem 1rem !important;
                    font-weight: 500 !important;
                    transition: transform .12s ease, opacity .12s ease;
                }
                .stButton > button:hover {
                    transform: translateY(-1px);
                    opacity: .95;
                }
                table {
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    padding: 8px 10px;
                    border-bottom: 1px solid #eee;
                }
                th {
                    color: #666;
                    font-weight: 600;
                }
                td {
                    color: #222;
                }
                .stTabs [data-baseweb="tab-list"] {
                    gap: .25rem;
                    margin-top: 1rem;
                }
                .stTabs [data-baseweb="tab"] {
                    padding: .6rem 1rem;
                }
                .streamlit-expanderHeader {
                    font-weight: 600;
                }
                #topbar-account {
                    margin-bottom: 1rem;
                }
                .food-card {
                    border: 1px solid #eee;
                    border-radius: 12px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    background-color: #f9f9f9;
                }
                .dish-name {
                    font-weight: bold;
                    font-size: 1.2em;
                }
                .stars {
                    font-size: 1.2em;
                    color: #FFD700;
                    text-align: right;
                }
                @media (max-width: 600px) {
                    .block-container {
                        padding-top: 4rem;
                        padding-left: 1rem;
                        padding-right: 1rem;
                    }
                    .stButton > button {
                        width: 100%;
                        margin-bottom: 0.5rem;
                    }
                    .stTabs [data-baseweb="tab-list"] {
                        margin-top: 0.5rem;
                    }
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        logger.error(f"Error injecting CSS: {e}")
        st.error("Cannot apply custom styling. Continuing with default.")

def current_user_id() -> Optional[int]:
    """Get current user ID from session state."""
    return st.session_state.get("user_id")

def initialize_session_state() -> None:
    """Initialize session state with default values."""
    defaults = {
        "user_id": None,
        "username": None,
        "language": "English",
        "editing_recipe_id": None,
        "recipe_form_data": {
            "title": "",
            "category": "",
            "instructions": "",
            "is_signature": False,
            "servings": 1.0,
            "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
        },
        "shopping_list_data": [],
        "adjusted_recipe": None,
        "search_value": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def topbar_account() -> None:
    """Display top bar with username, language selector, and logout button."""
    user_id = current_user_id()
    if not user_id:
        return
    with st.container():
        st.markdown('<div id="topbar-account">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"{get_text('username')}: {html.escape(st.session_state.get('username', 'Unknown'))}")
        with col2:
            st.selectbox(
                get_text("language"),
                ["English", "Vietnamese"],
                index=0 if st.session_state.get("language", "English") == "English" else 1,
                key="language_selector",
                on_change=lambda: st.session_state.update({"language": st.session_state.language_selector})
            )
        with col3:
            if st.button(get_text("logout"), key="logout_button"):
                st.session_state.clear()
                initialize_session_state()
                logger.info(f"User {st.session_state.get('username', 'Unknown')} logged out")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def calculate_stars(count: int, is_signature: bool) -> int:
    """Calculate stars based on cook count and signature status."""
    if not isinstance(count, int) or count < 0:
        return 0
    thresholds = [(15, 5), (8, 4), (5, 3), (3, 2), (1, 1)]
    return 5 if is_signature else next((stars for threshold, stars in thresholds if count >= threshold), 0)

def _norm_name(name: str) -> str:
    """Normalize ingredient name for comparison."""
    return (name or "").strip().lower()

def _norm_unit(unit: str) -> str:
    """Normalize unit for comparison."""
    return (unit or "").strip().lower()

def _inventory_map(user_id: int) -> Dict[Tuple[str, str], dict]:
    """Create inventory map based on normalized name and unit."""
    with Session() as session:
        try:
            items = session.query(Inventory).filter_by(user_id=user_id).all()
            return {
                (_norm_name(item.name), _norm_unit(item.unit)): {
                    "id": item.id,
                    "name": item.name,
                    "quantity": item.quantity,
                    "unit": item.unit
                }
                for item in items if item.name and item.unit
            }
        except SQLAlchemyError as e:
            logger.error(f"Error fetching inventory map for user {user_id}: {e}")
            raise

def validate_ingredients(recipe: Dict, inventory_map: Dict[Tuple[str, str], dict] = None) -> Tuple[bool, Optional[str]]:
    """Validate recipe ingredients and optionally check feasibility against inventory."""
    if not recipe.get("ingredients"):
        return False, get_text("error_ingredients_required")
    
    for ing in recipe.get("ingredients", []):
        name = _norm_name(ing.get("name", ""))
        unit = _norm_unit(ing.get("unit", ""))
        qty = float(ing.get("quantity", 0.0))
        is_spice = ing.get("is_spice", False)
        
        if not name or qty <= 0:
            return False, get_text("error_ingredients_required")
        if not DatabaseManager.validate_name(ing.get("name", "")):
            return False, get_text("error_invalid_name").format(name=ing.get("name"))
        if unit not in [_norm_unit(u) for u in VALID_UNITS]:
            return False, get_text("error_invalid_unit").format(unit=ing.get("unit"))
        if qty > MAX_QUANTITY:
            return False, get_text("error_excessive_qty").format(name=ing.get("name"), max_qty=MAX_QUANTITY, unit=ing.get("unit"))
        if not isinstance(is_spice, bool):
            return False, f"Invalid is_spice value for {ing.get('name')}: must be boolean"
        
        if inventory_map is not None:
            key = (name, unit)
            inv_item = inventory_map.get(key)
            if not inv_item:
                return False, f"Ingredient {ing.get('name')} not found in inventory"
            if inv_item["unit"] != ing.get("unit"):
                return False, f"Unit mismatch for {ing.get('name')}: expected {ing.get('unit')}, found {inv_item['unit']}"
            if inv_item["quantity"] < qty:
                return False, f"Insufficient quantity for {ing.get('name')}: need {qty}, have {inv_item['quantity']}"
    
    return True, None

def recipe_feasibility(recipe: Dict, user_id: int) -> Tuple[bool, List[Dict]]:
    """Check recipe feasibility based on inventory."""
    try:
        inv_map = _inventory_map(user_id)
        shorts = []
        feasible = True
        
        for ing in recipe.get("ingredients", []):
            name = _norm_name(ing.get("name", ""))
            unit = _norm_unit(ing.get("unit", ""))
            qty = float(ing.get("quantity", 0.0))
            key = (name, unit)
            inv_item = inv_map.get(key, {})
            have_qty = float(inv_item.get("quantity", 0.0))
            missing = max(0.0, qty - have_qty)
            
            if missing > 1e-9 or not inv_item:
                feasible = False
                shorts.append({
                    "name": ing.get("name", ""),
                    "needed_qty": qty,
                    "have_qty": have_qty,
                    "needed_unit": ing.get("unit", ""),
                    "have_unit": inv_item.get("unit", "") if inv_item else "",
                    "missing_qty_disp": missing,
                    "missing_unit_disp": ing.get("unit", "")
                })
        
        return feasible, shorts
    except SQLAlchemyError as e:
        logger.error(f"Error checking recipe feasibility: {e}")
        raise

def consume_ingredients_for_recipe(recipe: Dict, user_id: int) -> Tuple[bool, str]:
    """Consume ingredients from inventory if recipe is feasible."""
    with Session() as session:
        try:
            inv_map = _inventory_map(user_id)
            is_valid, error = validate_ingredients(recipe, inv_map)
            if not is_valid:
                logger.warning(f"Validation failed for recipe {recipe.get('title', 'Unknown')}: {error}")
                return False, get_text("cook_failed").format(error=error)
            
            for ing in recipe.get("ingredients", []):
                name = _norm_name(ing.get("name", ""))
                unit = _norm_unit(ing.get("unit", ""))
                qty = float(ing.get("quantity", 0.0))
                key = (name, unit)
                inv_item = inv_map.get(key)
                
                inventory_item = session.query(Inventory).filter_by(id=inv_item["id"]).first()
                inventory_item.quantity = max(0.0, inventory_item.quantity - qty)
            
            session.commit()
            logger.info(f"Successfully consumed ingredients for recipe {recipe.get('title', 'Unknown')}")
            return True, get_text("cook_success")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to consume ingredients for recipe {recipe.get('title', 'Unknown')}: {str(e)}")
            return False, get_text("cook_failed").format(error=str(e))

def normalize_quantity(quantity: Any) -> float:
    """Normalize quantity input to float, handling strings with commas or decimals."""
    if isinstance(quantity, (int, float)):
        return float(quantity)
    if isinstance(quantity, str):
        try:
            return float(quantity.replace(',', '.').strip())
        except ValueError:
            raise ValueError(get_text("invalid_quantity"))
    raise ValueError(get_text("invalid_quantity"))

class DatabaseManager:
    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate ingredient or user name, allowing Unicode characters."""
        return bool(name and name.strip() and all(c.isprintable() for c in name))

    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize name for comparison."""
        return _norm_name(name)

    @classmethod
    def verify_login(cls, username: str, password: str) -> Optional[int]:
        """Verify user login credentials."""
        if not username or not password or len(password) < 8:
            return None
        with Session() as session:
            try:
                user = session.query(User).filter_by(username=username).first()
                if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                    return user.id
                return None
            except SQLAlchemyError as e:
                logger.error(f"Error verifying login for {username}: {e}")
                raise

    @classmethod
    def create_user(cls, username: str, password: str, sec_question: str, sec_answer: str) -> Tuple[bool, str]:
        """Create a new user."""
        if not all([username.strip(), password.strip(), sec_question.strip(), sec_answer.strip()]):
            return False, "All fields required."
        if len(password) < 8:
            return False, "Password must be at least 8 characters."
        if not cls.validate_name(username):
            return False, get_text("error_invalid_name").format(name=username)
        
        with Session() as session:
            try:
                if session.query(User).filter_by(username=username).first():
                    return False, "Username already exists."
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                sec_answer_hash = bcrypt.hashpw(sec_answer.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user = User(
                    username=username,
                    password_hash=password_hash,
                    sec_question=sec_question,
                    sec_answer_hash=sec_answer_hash
                )
                session.add(user)
                session.commit()
                logger.info(f"Created user: {username}")
                return True, "User created successfully."
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error creating user {username}: {e}")
                return False, get_text("db_error").format(error=str(e))

    @classmethod
    def reset_password(cls, username: str, sec_answer: str, new_password: str) -> bool:
        """Reset user password."""
        if not all([username.strip(), sec_answer.strip(), new_password.strip()]):
            return False
        if len(new_password) < 8:
            return False
        with Session() as session:
            try:
                user = session.query(User).filter_by(username=username).first()
                if not user:
                    return False
                if bcrypt.checkpw(sec_answer.encode('utf-8'), user.sec_answer_hash.encode('utf-8')):
                    user.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    session.commit()
                    logger.info(f"Password reset for user: {username}")
                    return True
                return False
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error resetting password for {username}: {e}")
                return False

    @classmethod
    def list_inventory(cls, user_id: int) -> List[Dict]:
        """List user inventory."""
        with Session() as session:
            try:
                items = session.query(Inventory).filter_by(user_id=user_id).all()
                return [
                    {"id": item.id, "name": item.name, "quantity": item.quantity, "unit": item.unit}
                    for item in items
                ]
            except SQLAlchemyError as e:
                logger.error(f"Error listing inventory for user {user_id}: {e}")
                raise

    @classmethod
    def upsert_inventory(cls, user_id: int, name: str, quantity: float, unit: str) -> bool:
        """Add or update inventory item."""
        with Session() as session:
            try:
                if not cls.validate_name(name):
                    logger.error(f"Invalid name for inventory item: {name}")
                    return False
                if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
                    logger.error(f"Invalid unit for inventory item: {unit}")
                    return False
                if quantity < 0:
                    logger.error(f"Negative quantity for inventory item: {name}")
                    return False
                if quantity > MAX_QUANTITY:
                    logger.error(f"Excessive quantity for inventory item: {name}")
                    return False
                item = session.query(Inventory).filter_by(
                    user_id=user_id,
                    name=cls.normalize_name(name),
                    unit=_norm_unit(unit)
                ).first()
                if item:
                    item.quantity = max(0.0, item.quantity + quantity)
                else:
                    item = Inventory(
                        user_id=user_id,
                        name=name,
                        quantity=max(0.0, quantity),
                        unit=unit
                    )
                    session.add(item)
                session.commit()
                logger.info(f"Upserted inventory item: {name} for user {user_id}")
                return True
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error upserting inventory for user {user_id}: {e}")
                return False

    @classmethod
    def update_inventory_item(cls, user_id: int, item_id: int, name: str, quantity: float, unit: str) -> Tuple[bool, str]:
        """Update specific inventory item by ID."""
        with Session() as session:
            try:
                item = session.query(Inventory).filter_by(id=item_id, user_id=user_id).first()
                if not item:
                    logger.error(f"Inventory item not found: id={item_id}, user_id={user_id}")
                    return False, "Item not found."
                if not cls.validate_name(name):
                    logger.error(f"Invalid name for inventory item: {name}")
                    return False, get_text("error_invalid_name").format(name=name)
                if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
                    logger.error(f"Invalid unit for inventory item: {unit}")
                    return False, get_text("error_invalid_unit").format(unit=unit)
                if quantity < 0:
                    logger.error(f"Negative quantity for inventory item: {name}")
                    return False, get_text("error_negative_qty").format(name=name)
                if quantity > MAX_QUANTITY:
                    logger.error(f"Excessive quantity for inventory item: {name}")
                    return False, get_text("error_excessive_qty").format(name=name, max_qty=MAX_QUANTITY, unit=unit)
                item.name = name
                item.quantity = max(0.0, quantity)
                item.unit = unit
                session.commit()
                logger.info(f"Updated inventory item: id={item_id} for user {user_id}")
                return True, "Inventory item updated successfully."
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error updating inventory item {item_id}: {e}")
                return False, get_text("db_error").format(error=str(e))

    @classmethod
    def delete_inventory(cls, user_id: int, item_id: int) -> bool:
        """Delete inventory item by ID."""
        with Session() as session:
            try:
                item = session.query(Inventory).filter_by(id=item_id, user_id=user_id).first()
                if item:
                    session.delete(item)
                    session.commit()
                    logger.info(f"Deleted inventory item: id={item_id} for user {user_id}")
                    return True
                return False
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error deleting inventory item {item_id}: {e}")
                return False

    @classmethod
    def list_recipes(cls, user_id: int) -> List[Dict]:
        """List user recipes with ingredients."""
        with Session() as session:
            try:
                recipes = session.query(Recipe).filter_by(user_id=user_id).all()
                return [
                    {
                        "id": r.id,
                        "title": r.title,
                        "category": r.category,
                        "instructions": r.instructions,
                        "servings": r.servings,
                        "is_signature": r.is_signature,
                        "ingredients": [
                            {
                                "name": i.name,
                                "quantity": i.quantity,
                                "unit": i.unit,
                                "is_spice": i.is_spice
                            } for i in r.ingredients
                        ]
                    } for r in recipes
                ]
            except SQLAlchemyError as e:
                logger.error(f"Error listing recipes for user {user_id}: {e}")
                raise

    @classmethod
    def create_recipe(cls, user_id: int, title: str, category: str, instructions: str, 
                     ingredients: List[Dict], recipe_id: Optional[int] = None, is_signature: bool = False) -> Tuple[bool, str]:
        """Create or update a recipe with validation."""
        with Session() as session:
            try:
                if not title.strip():
                    return False, get_text("error_title_required")
                if not instructions.strip() or len(instructions.strip()) < 10:
                    return False, "Instructions must be at least 10 characters long."
                if not any(ing["name"].strip() and ing["quantity"] > 0 for ing in ingredients):
                    return False, get_text("error_ingredients_required")
                
                # Validate ingredients
                for ing in ingredients:
                    if not cls.validate_name(ing["name"]):
                        return False, get_text("error_invalid_name").format(name=ing["name"])
                    if _norm_unit(ing["unit"]) not in [_norm_unit(u) for u in VALID_UNITS]:
                        return False, get_text("error_invalid_unit").format(unit=ing["unit"])
                    if ing["quantity"] <= 0:
                        return False, get_text("error_negative_qty").format(name=ing["name"])
                    if ing["quantity"] > MAX_QUANTITY:
                        return False, get_text("error_excessive_qty").format(name=ing["name"], max_qty=MAX_QUANTITY, unit=ing["unit"])
                    if not isinstance(ing.get("is_spice", False), bool):
                        return False, f"Invalid is_spice value for {ing['name']}: must be boolean"
                
                # Check for duplicate title
                if session.query(Recipe).filter_by(user_id=user_id, title=title).filter(Recipe.id != recipe_id).first():
                    return False, get_text("duplicate_recipe")
                
                # Update or create recipe
                if recipe_id:
                    recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
                    if not recipe:
                        return False, get_text("delete_failed").format(title=title, error="Recipe not found")
                    recipe.title = title
                    recipe.category = category
                    recipe.instructions = instructions
                    recipe.is_signature = is_signature
                    recipe.servings = 1.0
                    session.query(RecipeIngredient).filter_by(recipe_id=recipe_id).delete()
                else:
                    recipe = Recipe(
                        user_id=user_id,
                        title=title,
                        category=category,
                        instructions=instructions,
                        servings=1.0,
                        is_signature=is_signature
                    )
                    session.add(recipe)
                    session.flush()
                
                # Add ingredients
                ingredients_to_add = [
                    RecipeIngredient(
                        recipe_id=recipe.id,
                        name=ing["name"],
                        quantity=ing["quantity"],
                        unit=ing["unit"],
                        is_spice=ing.get("is_spice", False)
                    ) for ing in ingredients
                ]
                session.bulk_save_objects(ingredients_to_add)
                
                session.commit()
                logger.info(f"{'Updated' if recipe_id else 'Created'} recipe: {title} for user {user_id}")
                return True, get_text("update_success" if recipe_id else "save_success").format(title=title)
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error saving recipe {title}: {e}")
                return False, get_text("save_failed").format(title=title, error=str(e))

    @classmethod
    def delete_recipe(cls, user_id: int, recipe_id: int) -> Tuple[bool, str]:
        """Delete a recipe and its related records."""
        with Session() as session:
            try:
                recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
                if not recipe:
                    return False, get_text("delete_failed").format(title="Unknown", error="Recipe not found")
                
                # Check for dependencies and delete related records
                history_count = session.query(CookedHistory).filter_by(recipe_id=recipe_id).count()
                if history_count > 0:
                    logger.info(f"Deleting {history_count} cooked history records for recipe {recipe_id}")
                    session.query(CookedHistory).filter_by(recipe_id=recipe_id).delete()
                
                session.delete(recipe)
                session.commit()
                logger.info(f"Deleted recipe: id={recipe_id} for user {user_id}")
                return True, get_text("delete_success").format(title=recipe.title)
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Integrity error deleting recipe {recipe_id}: {e}")
                return False, get_text("delete_failed").format(title=recipe.title if 'recipe' in locals() else "Unknown", error="Recipe is referenced elsewhere")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error deleting recipe {recipe_id}: {e}")
                return False, get_text("delete_failed").format(title=recipe.title if 'recipe' in locals() else "Unknown", error=str(e))

    @classmethod
    def log_cooked_recipe(cls, user_id: int, recipe_id: int) -> bool:
        """Log a cooked recipe."""
        with Session() as session:
            try:
                session.add(CookedHistory(user_id=user_id, recipe_id=recipe_id))
                session.commit()
                logger.info(f"Logged cooked recipe: id={recipe_id} for user {user_id}")
                return True
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error logging cooked recipe {recipe_id}: {e}")
                return False

    @classmethod
    def list_cooked_history(cls, user_id: int) -> List[Dict]:
        """List cooking history."""
        with Session() as session:
            try:
                history = session.query(CookedHistory).filter_by(user_id=user_id).all()
                return [
                    {"recipe_id": h.recipe_id, "cooked_date": h.cooked_date.strftime("%Y-%m-%d %H:%M:%S")}
                    for h in history
                ]
            except SQLAlchemyError as e:
                logger.error(f"Error listing cooked history for user {user_id}: {e}")
                raise

    @classmethod
    def get_cooked_count(cls, user_id: int, recipe_id: int) -> int:
        """Get count of times a recipe was cooked."""
        with Session() as session:
            try:
                return session.query(CookedHistory).filter_by(user_id=user_id, recipe_id=recipe_id).count()
            except SQLAlchemyError as e:
                logger.error(f"Error getting cooked count for recipe {recipe_id}: {e}")
                raise

def inventory_page() -> None:
    """Display and manage ingredient inventory."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return
    inventory_key = f"inventory_data_{user_id}"
    try:
        inventory = DatabaseManager.list_inventory(user_id)
        st.session_state[inventory_key] = inventory
    except SQLAlchemyError as e:
        logger.error(f"Error loading inventory for user {user_id}: {e}")
        st.error(get_text("db_error").format(error=str(e)))
        return

    st.header(get_text("inventory"))
    st.subheader(get_text("your_stock"))
    st.caption(get_text("unit_tips"))

    with st.expander(get_text("add_ingredient")):
        with st.form(key="add_inventory_form"):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                ingredient_name = st.text_input(get_text("name"), placeholder="e.g., chicken", key="new_ingredient_name")
            with col2:
                quantity_input = st.text_input(get_text("quantity"), value="0.0", key="new_quantity")
            with col3:
                unit = st.selectbox(get_text("unit"), options=VALID_UNITS, key="new_unit")
            if st.form_submit_button(get_text("add_ingredient")):
                try:
                    quantity = normalize_quantity(quantity_input)
                    if not ingredient_name.strip():
                        st.error(get_text("error_ingredients_required"))
                    elif not DatabaseManager.validate_name(ingredient_name):
                        st.error(get_text("error_invalid_name").format(name=ingredient_name))
                    elif _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
                        st.error(get_text("error_invalid_unit").format(unit=unit))
                    elif quantity < 0:
                        st.error(get_text("error_negative_qty").format(name=ingredient_name))
                    elif quantity > MAX_QUANTITY:
                        st.error(get_text("error_excessive_qty").format(name=ingredient_name, max_qty=MAX_QUANTITY, unit=unit))
                    else:
                        if DatabaseManager.upsert_inventory(user_id, ingredient_name.strip(), quantity, unit):
                            st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                            st.success(get_text("save_success").format(title=ingredient_name))
                            st.rerun()
                        else:
                            st.error(get_text("save_failed").format(title=ingredient_name, error="Could not add ingredient"))
                except ValueError as e:
                    st.error(str(e))
                except SQLAlchemyError as e:
                    logger.error(f"Error adding ingredient {ingredient_name}: {e}")
                    st.error(get_text("db_error").format(error=str(e)))

    edited_data = st.data_editor(
        inventory,
        column_config={
            "id": None,
            "name": st.column_config.TextColumn(get_text("name"), required=True),
            "quantity": st.column_config.NumberColumn(
                get_text("quantity"),
                min_value=0.0,
                max_value=MAX_QUANTITY,
                format="%.2f",
                required=True
            ),
            "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
        },
        num_rows="dynamic",
        key=f"inventory_editor_{user_id}",
        hide_index=True
    )

    if st.button(get_text("save_changes"), key="save_inventory_changes"):
        errors = []
        validated_data = []
        for item in edited_data:
            name = item.get("name", "").strip()
            unit = item.get("unit", "")
            quantity = item.get("quantity")
            if not name or quantity is None or not unit:
                errors.append(get_text("error_ingredients_required"))
                continue
            if not DatabaseManager.validate_name(name):
                errors.append(get_text("error_invalid_name").format(name=name))
                continue
            if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
                errors.append(get_text("error_invalid_unit").format(unit=unit))
                continue
            if quantity < 0:
                errors.append(get_text("error_negative_qty").format(name=name))
                continue
            if quantity > MAX_QUANTITY:
                errors.append(get_text("error_excessive_qty").format(name=name, max_qty=MAX_QUANTITY, unit=unit))
                continue
            validated_data.append({"id": item.get("id"), "name": name, "quantity": float(quantity), "unit": unit})

        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                old_ids = {item.get("id") for item in inventory if item.get("id")}
                edited_ids = {item.get("id") for item in validated_data if item.get("id")}
                deleted_ids = old_ids - edited_ids
                for item_id in deleted_ids:
                    if DatabaseManager.delete_inventory(user_id, item_id):
                        logger.info(f"Deleted inventory item: id={item_id} for user {user_id}")
                for item in validated_data:
                    if item.get("id"):
                        success, message = DatabaseManager.update_inventory_item(user_id, item["id"], item["name"], item["quantity"], item["unit"])
                        if not success:
                            st.error(message)
                            continue
                    else:
                        if not DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"]):
                            st.error(get_text("save_failed").format(title=item["name"], error="Could not add ingredient"))
                            continue
                st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                st.success(get_text("inventory_updated"))
                st.rerun()
            except SQLAlchemyError as e:
                logger.error(f"Error updating inventory: {e}")
                st.error(get_text("db_error").format(error=str(e)))

    if not inventory:
        st.info(get_text("no_ingredients"))

def recipes_page() -> None:
    """Display and manage user recipes."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return
    try:
        recipes = DatabaseManager.list_recipes(user_id)
    except SQLAlchemyError as e:
        logger.error(f"Error loading recipes for user {user_id}: {e}")
        st.error(get_text("db_error").format(error=str(e)))
        return

    st.header(get_text("recipes"))
    st.subheader(get_text("your_recipes"))
    st.caption(get_text("unit_tips"))

    if not recipes:
        st.info(get_text("no_recipes"))

    form_data = st.session_state.recipe_form_data
    recipe_id = st.session_state.get("editing_recipe_id")

    with st.form(key="recipe_form"):
        title = st.text_input(get_text("title"), value=form_data["title"], key="recipe_title")
        category = st.text_input(get_text("category"), value=form_data["category"], key="recipe_category")
        instructions = st.text_area(get_text("instructions"), value=form_data["instructions"], key="recipe_instructions")
        is_signature = st.checkbox(get_text("signature_dish"), value=form_data["is_signature"], key="recipe_is_signature")
        ingredients_data = st.data_editor(
            form_data["ingredients"],
            column_config={
                "name": st.column_config.TextColumn(get_text("name"), required=True),
                "quantity": st.column_config.NumberColumn(
                    get_text("quantity"),
                    min_value=0.0,
                    max_value=MAX_QUANTITY,
                    format="%.2f",
                    required=True
                ),
                "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
                "is_spice": st.column_config.CheckboxColumn("Spice", default=False)
            },
            num_rows="dynamic",
            key="ingredients_editor",
            hide_index=True
        )

        submit_label = get_text("update_recipe") if recipe_id else get_text("save_recipe")
        if st.form_submit_button(submit_label):
            if not title.strip():
                st.error(get_text("error_title_required"))
                return
            if not instructions.strip() or len(instructions.strip()) < 10:
                st.error("Hướng dẫn phải có ít nhất 10 ký tự.")
                return
            valid_ingredients = []
            for ing in ingredients_data:
                name = ing.get("name", "").strip()
                quantity = ing.get("quantity")
                unit = ing.get("unit", "")
                is_spice = ing.get("is_spice", False)
                if not name or quantity is None or not unit:
                    st.error(get_text("error_ingredients_required"))
                    return
                if not DatabaseManager.validate_name(name):
                    st.error(get_text("error_invalid_name").format(name=name))
                    return
                if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
                    st.error(get_text("error_invalid_unit").format(unit=unit))
                    return
                if quantity <= 0:
                    st.error(get_text("error_negative_qty").format(name=name))
                    return
                if quantity > MAX_QUANTITY:
                    st.error(get_text("error_excessive_qty").format(name=name, max_qty=MAX_QUANTITY, unit=unit))
                    return
                if not isinstance(is_spice, bool):
                    st.error(f"Giá trị is_spice không hợp lệ cho {name}: phải là boolean")
                    return
                valid_ingredients.append({
                    "name": name,
                    "quantity": float(quantity),
                    "unit": unit,
                    "is_spice": is_spice
                })
            if not valid_ingredients:
                st.error(get_text("error_ingredients_required"))
                return
            existing_recipe = next((r for r in recipes if r.get("title") == title.strip() and r.get("id") != recipe_id), None)
            if existing_recipe:
                st.error(get_text("duplicate_recipe"))
                return
            try:
                success, message = DatabaseManager.create_recipe(
                    user_id, title.strip(), category.strip(), instructions.strip(), 
                    valid_ingredients, recipe_id, is_signature
                )
                if success:
                    st.success(message)
                    st.session_state.recipe_form_data = {
                        "title": "",
                        "category": "",
                        "instructions": "",
                        "is_signature": False,
                        "servings": 1.0,
                        "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
                    }
                    st.session_state.editing_recipe_id = None
                    st.rerun()
                else:
                    st.error(message)
            except SQLAlchemyError as e:
                logger.error(f"Error saving recipe {title}: {e}")
                st.error(get_text("save_failed").format(title=title, error=str(e)))

    if recipes:
        for recipe in recipes:
            signature_text = f" - {get_text('signature_dish')}" if recipe.get("is_signature") else ""
            with st.expander(f"{html.escape(recipe.get('title', 'Untitled'))} ({html.escape(recipe.get('category', '-'))}) {signature_text}"):
                st.write(f"**{get_text('instructions')}:** {html.escape(recipe.get('instructions', ''))}")
                st.table([
                    {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
                     get_text("unit"): ing["unit"], "Spice": "Yes" if ing.get("is_spice") else "No"}
                    for ing in recipe.get("ingredients", [])
                ])
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(get_text("update_recipe"), key=f"edit_{recipe.get('id')}"):
                        st.session_state.editing_recipe_id = recipe["id"]
                        st.session_state.recipe_form_data = {
                            "title": recipe["title"],
                            "category": recipe["category"],
                            "instructions": recipe["instructions"],
                            "is_signature": recipe.get("is_signature", False),
                            "servings": recipe.get("servings", 1.0),
                            "ingredients": [
                                {"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": ing.get("is_spice", False)}
                                for ing in recipe.get("ingredients", [])
                            ]
                        }
                        st.rerun()
                with col2:
                    if st.button(get_text("delete_recipe"), key=f"delete_{recipe.get('id')}"):
                        try:
                            success, message = DatabaseManager.delete_recipe(user_id, recipe["id"])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        except SQLAlchemyError as e:
                            logger.error(f"Error deleting recipe {recipe['title']}: {e}")
                            st.error(get_text("delete_failed").format(title=recipe["title"], error=str(e)))

def feasibility_page() -> None:
    """Display recipe feasibility and shopping list options."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return
    inventory_key = f"inventory_data_{user_id}"
    try:
        recipes = DatabaseManager.list_recipes(user_id)
        inventory = DatabaseManager.list_inventory(user_id)
        st.session_state[inventory_key] = inventory
    except SQLAlchemyError as e:
        logger.error(f"Error loading data for user {user_id}: {e}")
        st.error(get_text("db_error").format(error=str(e)))
        return

    if not recipes:
        st.info(get_text("create_recipes_first"))
        return

    st.header(get_text("feasibility"))
    st.subheader(get_text("you_can_cook"))

    recipe_results = [
        {"recipe": r, "feasible": feasible, "shorts": shorts}
        for r in recipes
        for feasible, shorts in [recipe_feasibility(r, user_id)]
    ]

    if not recipe_results:
        st.info(get_text("none_yet"))
        return

    if all(r["feasible"] for r in recipe_results):
        st.success(get_text("all_feasible"))

    selected_titles = st.multiselect(
        get_text("select_recipes_label"),
        [r["recipe"]["title"] for r in recipe_results],
        format_func=lambda t: f"{t} {'✅' if next((r for r in recipe_results if r['recipe']['title'] == t), {}).get('feasible', False) else '❌'}",
        key="select_recipes_feasibility"
    )

    selected_missing = []
    for result in [r for r in recipe_results if r["recipe"]["title"] in selected_titles]:
        st.markdown(f"#### {html.escape(result['recipe'].get('title', 'Untitled'))}")
        if result["feasible"]:
            st.success(get_text("all_available"))
            if st.button(get_text("cook"), key=f"cook_{result['recipe'].get('id')}"):
                try:
                    success, message = consume_ingredients_for_recipe(result["recipe"], user_id)
                    if success:
                        DatabaseManager.log_cooked_recipe(user_id, result["recipe"]["id"])
                        count = DatabaseManager.get_cooked_count(user_id, result["recipe"]["id"])
                        stars = calculate_stars(count, result["recipe"].get("is_signature", False))
                        previous_stars = calculate_stars(count - 1, result["recipe"].get("is_signature", False))
                        if stars > previous_stars:
                            st.success(get_text("congrats").format(stars="⭐" * stars, dish=result["recipe"]["title"]))
                        st.success(message)
                        st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                        st.rerun()
                    else:
                        st.error(message)
                        _, shorts = recipe_feasibility(result["recipe"], user_id)
                        if shorts:
                            st.table([
                                {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
                                 get_text("have"): f"{s['have_qty']} {s['have_unit']}",
                                 get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
                                for s in shorts
                            ])
                except SQLAlchemyError as e:
                    logger.error(f"Error cooking recipe {result['recipe']['title']}: {e}")
                    st.error(get_text("db_error").format(error=str(e)))
        else:
            st.warning(get_text("missing_something"))
            st.table([
                {get_text("name"): s["name"], get_text("need"): s["needed_qty"], get_text("have"): s["have_qty"],
                 get_text("unit"): s["needed_unit"], get_text("missing"): s["missing_qty_disp"]}
                for s in result["shorts"]
            ])
            selected_missing.extend(result["shorts"])

    if selected_missing and st.button(get_text("add_to_shopping"), key="add_to_shopping_feasibility"):
        try:
            agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
            for s in selected_missing:
                key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
                agg_missing[key]["name"] = s["name"]
                agg_missing[key]["quantity"] += s["missing_qty_disp"]
                agg_missing[key]["unit"] = s["missing_unit_disp"]
            st.session_state["shopping_list_data"] = list(agg_missing.values())
            st.success(get_text("sent_to_shopping"))
            st.rerun()
        except SQLAlchemyError as e:
            logger.error(f"Error adding to shopping list: {e}")
            st.error(get_text("db_error").format(error=str(e)))

def shopping_list_page() -> None:
    """Manage shopping list and update inventory."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return
    inventory_key = f"inventory_data_{user_id}"
    try:
        inventory = DatabaseManager.list_inventory(user_id)
        st.session_state[inventory_key] = inventory
    except SQLAlchemyError as e:
        logger.error(f"Error loading inventory for user {user_id}: {e}")
        st.error(get_text("db_error").format(error=str(e)))
        return

    shopping_list = st.session_state.get("shopping_list_data", [])
    st.header(get_text("shopping_list"))
    if not shopping_list:
        st.info(get_text("empty_list"))
        return

    valid_shopping_list = []
    for item in shopping_list:
        try:
            quantity = normalize_quantity(item.get("quantity", 0.0))
            if (isinstance(item, dict) and
                    item.get("name") and isinstance(item.get("name"), str) and
                    quantity >= 0 and
                    item.get("unit") and _norm_unit(item["unit"]) in [_norm_unit(u) for u in VALID_UNITS]):
                valid_shopping_list.append({
                    "name": item["name"],
                    "quantity": quantity,
                    "unit": item["unit"]
                })
            else:
                logger.warning(f"Invalid shopping list item: {item}")
        except ValueError as e:
            logger.warning(f"Invalid quantity in shopping list item: {item}, error: {e}")
    shopping_list = valid_shopping_list
    st.session_state["shopping_list_data"] = shopping_list

    shopping_data = st.data_editor(
        shopping_list,
        column_config={
            "name": st.column_config.TextColumn(get_text("name"), required=True),
            "quantity": st.column_config.NumberColumn(
                get_text("quantity"),
                min_value=0.0,
                format="%.2f",
                required=True
            ),
            "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
        },
        num_rows="dynamic",
        key="shopping_list_editor",
        hide_index=True
    )

    validated_shopping_data = []
    errors = []
    for item in shopping_data:
        name = item.get("name", "").strip()
        quantity = item.get("quantity")
        unit = item.get("unit", "")
        if not name or quantity is None or not unit:
            errors.append(get_text("error_ingredients_required"))
            continue
        if not DatabaseManager.validate_name(name):
            errors.append(get_text("error_invalid_name").format(name=name))
            continue
        if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
            errors.append(get_text("error_invalid_unit").format(unit=unit))
            continue
        if quantity < 0:
            errors.append(get_text("error_negative_qty").format(name=name))
            continue
        validated_shopping_data.append({
            "name": name,
            "quantity": float(quantity),
            "unit": unit
        })

    if errors:
        for error in errors:
            st.error(error)
        return

    st.session_state["shopping_list_data"] = validated_shopping_data

    purchased_labels = [f"{item['name']} ({item['unit']})" for item in validated_shopping_data if item.get("name") and item.get("unit")]
    purchased_names = st.multiselect(get_text("select_purchased"), options=purchased_labels, key="select_purchased_shopping")

    if st.button(get_text("update_inventory"), key="update_inventory_shopping"):
        try:
            for item in validated_shopping_data:
                item_label = f"{item['name']} ({item['unit']})"
                if item_label in purchased_names:
                    if not DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"]):
                        st.error(get_text("save_failed").format(title=item["name"], error="Could not update inventory"))
                        continue
            st.session_state["shopping_list_data"] = [
                item for item in validated_shopping_data if f"{item['name']} ({item['unit']})" not in purchased_names
            ]
            st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
            st.success(get_text("purchased"))
            st.rerun()
        except SQLAlchemyError as e:
            logger.error(f"Error updating inventory from shopping list: {e}")
            st.error(get_text("db_error").format(error=str(e)))

def adjust_recipe(recipe: Dict, adjustment_type: str, new_servings: float, new_quantity: float, 
                 main_ingredient: str, spice_factor: float) -> Tuple[Dict, Optional[str]]:
    """Adjust recipe based on servings or main ingredient, with spice level scaling."""
    try:
        # Initialize adjusted recipe
        adjusted_recipe = {
            "id": recipe.get("id"),
            "title": get_text("adjusted_recipe_title").format(title=recipe.get("title")),
            "category": recipe.get("category"),
            "instructions": recipe.get("instructions"),
            "servings": recipe.get("servings", 1.0),
            "ingredients": [],
            "origin_id": recipe.get("id"),
            "tag": "adjusted"
        }

        # Calculate adjustment ratio
        adjustment_ratio = 1.0
        if adjustment_type == get_text("by_servings"):
            base_servings = float(recipe.get("servings", 1.0))
            if base_servings == 0:
                return adjusted_recipe, get_text("invalid_adjustment") + ": Base servings cannot be zero."
            if new_servings <= 0:
                return adjusted_recipe, get_text("invalid_adjustment") + ": New servings must be positive."
            adjustment_ratio = new_servings / base_servings
            adjusted_recipe["servings"] = new_servings
        else:
            main_ingredients = [ing for ing in recipe.get("ingredients", []) if not ing.get("is_spice", False)]
            if not main_ingredients:
                return adjusted_recipe, get_text("error_ingredients_required")
            selected_ing = next((ing for ing in main_ingredients if ing.get("name") == main_ingredient), None)
            if not selected_ing:
                return adjusted_recipe, get_text("invalid_adjustment") + ": Selected main ingredient not found."
            base_qty = float(selected_ing.get("quantity", 1.0))
            if base_qty == 0:
                return adjusted_recipe, get_text("invalid_adjustment") + ": Base quantity cannot be zero."
            if new_quantity <= 0:
                return adjusted_recipe, get_text("invalid_adjustment") + ": New quantity must be positive."
            adjustment_ratio = new_quantity / base_qty

        # Adjust ingredients
        for ing in recipe.get("ingredients", []):
            try:
                base_qty = float(ing.get("quantity", 0.0))
                new_qty = base_qty * adjustment_ratio * (spice_factor if ing.get("is_spice", False) else 1.0)
                new_qty = max(0.0, new_qty)  # Ensure non-negative
                adjusted_recipe["ingredients"].append({
                    "name": ing.get("name"),
                    "quantity": new_qty,
                    "unit": ing.get("unit"),
                    "is_spice": ing.get("is_spice", False)
                })
            except ValueError:
                return adjusted_recipe, get_text("invalid_quantity")

        return adjusted_recipe, None
    except Exception as e:
        return adjusted_recipe, get_text("invalid_adjustment") + f": {str(e)}"

def display_adjusted_recipe(adjusted_recipe: Dict) -> None:
    """Display the adjusted recipe in the UI."""
    st.subheader(get_text("adjusted_recipe"))
    st.write(f"**{get_text('title')}:** {html.escape(adjusted_recipe['title'])}")
    st.write(f"**{get_text('category')}:** {html.escape(adjusted_recipe.get('category', ''))}")
    st.write(f"**{get_text('servings')}:** {float(adjusted_recipe.get('servings', 0.0)):.2f}")
    st.write(f"**{get_text('instructions')}:** {html.escape(adjusted_recipe.get('instructions', ''))}")
    st.table([
        {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
         get_text("unit"): ing["unit"], "Spice": "Yes" if ing["is_spice"] else "No"}
        for ing in adjusted_recipe["ingredients"]
    ])

def recipe_adjustment_page() -> None:
    """Adjust recipes based on servings or main ingredient."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return
    inventory_key = f"inventory_data_{user_id}"
    try:
        inventory = DatabaseManager.list_inventory(user_id)
        st.session_state[inventory_key] = inventory
    except SQLAlchemyError as e:
        logger.error(f"Error loading data for adjustment for user {user_id}: {e}")
        st.error(get_text("db_error").format(error=str(e)))
        return

    if len(inventory) == 0:
        st.warning(get_text("empty_inventory_warning"))

    st.header(get_text("adjust_recipe"))
    try:
        recipes = DatabaseManager.list_recipes(user_id)
    except SQLAlchemyError as e:
        logger.error(f"Error loading recipes for user {user_id}: {e}")
        st.error(get_text("db_error").format(error=str(e)))
        return

    if not recipes:
        st.info(get_text("no_recipes"))
        return

    selected_recipe_title = st.selectbox(get_text("select_recipe"), [r.get("title") for r in recipes], key="select_recipe_adjust")
    if not selected_recipe_title:
        st.warning(get_text("no_recipe_selected"))
        return

    recipe = next(r for r in recipes if r.get("title") == selected_recipe_title)
    adjustment_type = st.radio(get_text("adjustment_type"), [get_text("by_servings"), get_text("by_main_ingredient")], key="adjustment_type_radio")

    new_servings = 0.0
    new_quantity = 0.0
    main_ingredient = ""
    if adjustment_type == get_text("by_servings"):
        base_servings = float(recipe.get("servings", 1.0))
        new_servings = st.number_input(get_text("new_servings"), value=base_servings, key="new_servings_input")
    else:
        main_ingredients = [ing for ing in recipe.get("ingredients", []) if not ing.get("is_spice", False)]
        if not main_ingredients:
            st.error(get_text("error_ingredients_required"))
            return
        main_ingredient = st.selectbox(get_text("main_ingredient"), [ing.get("name") for ing in main_ingredients], key="main_ingredient_select")
        selected_ing = next(ing for ing in main_ingredients if ing.get("name") == main_ingredient)
        base_qty = float(selected_ing.get("quantity", 1.0))
        new_quantity = st.number_input(get_text("new_quantity"), value=base_qty, key="new_quantity_input")

    spice_display_to_key = {
        get_text("mild"): "mild",
        get_text("normal"): "normal",
        get_text("rich"): "rich"
    }
    spice_level = st.radio(get_text("spice_level"), [get_text("mild"), get_text("normal"), get_text("rich")], key="spice_level_radio")
    spice_key = spice_display_to_key.get(spice_level, "normal")
    spice_factor = {"mild": 0.6, "normal": 0.8, "rich": 1.0}[spice_key]

    adjusted_recipe, error = adjust_recipe(recipe, adjustment_type, new_servings, new_quantity, main_ingredient, spice_factor)
    if error:
        st.error(error)
        return

    st.session_state["adjusted_recipe"] = adjusted_recipe
    display_adjusted_recipe(adjusted_recipe)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("cook_adjusted"), key="cook_adjusted_button"):
            with Session() as session:
                try:
                    feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
                    if not feasible:
                        st.error(get_text("insufficient_ingredients"))
                        if shorts:
                            st.table([
                                {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
                                 get_text("have"): f"{s['have_qty']} {s['have_unit']}",
                                 get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
                                for s in shorts
                            ])
                    else:
                        success, message = consume_ingredients_for_recipe(adjusted_recipe, user_id)
                        if success:
                            DatabaseManager.log_cooked_recipe(user_id, adjusted_recipe["origin_id"])
                            count = DatabaseManager.get_cooked_count(user_id, adjusted_recipe["origin_id"])
                            stars = calculate_stars(count, recipe.get("is_signature", False))
                            previous_stars = calculate_stars(count - 1, recipe.get("is_signature", False))
                            if stars > previous_stars:
                                st.success(get_text("congrats").format(stars="⭐" * stars, dish=adjusted_recipe["title"]))
                            st.success(get_text("cook_adjusted_success").format(title=adjusted_recipe["title"]))
                            st.session_state.pop("adjusted_recipe", None)
                            st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                            st.rerun()
                        else:
                            st.error(get_text("cook_adjusted_failed").format(title=adjusted_recipe["title"], error=message))
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    logger.error(f"Error cooking adjusted recipe {adjusted_recipe['title']}: {e}")
                    st.error(get_text("db_error").format(error=str(e)))

    with col2:
        if st.button(get_text("add_to_shopping_adjusted"), key="add_to_shopping_adjusted_button"):
            try:
                feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
                if not feasible:
                    agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
                    for s in shorts:
                        key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
                        agg_missing[key]["name"] = s["name"]
                        agg_missing[key]["quantity"] += s["missing_qty_disp"]
                        agg_missing[key]["unit"] = s["missing_unit_disp"]
                    new_shopping_list = list(agg_missing.values())
                    st.session_state["shopping_list_data"] = new_shopping_list
                    st.success(get_text("sent_to_shopping"))
                    st.rerun()
                else:
                    st.info(get_text("all_available"))
            except SQLAlchemyError as e:
                logger.error(f"Error adding adjusted recipe to shopping list: {e}")
                st.error(get_text("db_error").format(error=str(e)))

def food_timeline_page() -> None:
    """Display cooking history as a timeline."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return
    try:
        recipes = DatabaseManager.list_recipes(user_id)
        history = DatabaseManager.list_cooked_history(user_id)
    except SQLAlchemyError as e:
        logger.error(f"Error loading data for timeline for user {user_id}: {e}")
        st.error(get_text("db_error").format(error=str(e)))
        return

    st.header(get_text("food_timeline"))
    if not history:
        st.info(get_text("no_history"))
        return

    recipe_map = {r["id"]: r for r in recipes}
    search = st.text_input(get_text("search_placeholder"), key="timeline_search", value=st.session_state.get("search_value", ""))
    st.session_state["search_value"] = search

    filtered_history = []
    for entry in history:
        recipe = recipe_map.get(entry["recipe_id"], {"title": "Unknown", "is_signature": False})
        count = DatabaseManager.get_cooked_count(user_id, entry["recipe_id"])
        stars = calculate_stars(count, recipe.get("is_signature", False))
        entry_data = {
            "recipe_id": entry["recipe_id"],
            "title": recipe["title"],
            "cooked_date": entry["cooked_date"],
            "stars": stars,
            "is_signature": recipe.get("is_signature", False)
        }
        if not search:
            filtered_history.append(entry_data)
        else:
            search_lower = search.lower()
            date = datetime.strptime(entry["cooked_date"], "%Y-%m-%d %H:%M:%S")
            week = date.isocalendar()[1]
            searches = [s.strip() for s in search_lower.split(",")]
            match = False
            for s in searches:
                if s.startswith("tag:signature") and entry_data["is_signature"]:
                    match = True
                elif s.startswith("week:") and s[5:].isdigit() and int(s[5:]) == week:
                    match = True
                elif s.startswith("day:") and s[4:] in entry["cooked_date"]:
                    match = True
                elif search_lower in entry_data["title"].lower():
                    match = True
            if match:
                filtered_history.append(entry_data)

    if not filtered_history:
        st.info(get_text("no_entries"))
        return

    if st.button(get_text("reset_filter"), key="reset_timeline_filter"):
        st.session_state["search_value"] = ""
        st.rerun()

    dish_counts = Counter(h["title"] for h in filtered_history)
    if dish_counts:
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        week_end = week_start + timedelta(days=6)
        week_history = [
            h for h in filtered_history
            if week_start <= datetime.strptime(h["cooked_date"], "%Y-%m-%d %H:%M:%S") <= week_end
        ]
        week_counts = Counter(h["title"] for h in week_history)
        most_common = week_counts.most_common(1)
        if most_common:
            st.write(get_text("stats_week").format(
                count=len(week_history),
                dish=most_common[0][0]
            ))

    for entry in sorted(filtered_history, key=lambda x: x["cooked_date"], reverse=True):
        with st.container():
            st.markdown('<div class="food-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f'<span class="dish-name">{html.escape(entry["title"])}</span>', unsafe_allow_html=True)
                st.write(f"{entry['cooked_date']}")
            with col2:
                st.markdown(f'<span class="stars">{"⭐" * entry["stars"]}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def auth_gate_tabs() -> None:
    """Display authentication tabs for login, register, and reset password."""
    tabs = st.tabs([get_text("login"), get_text("register"), get_text("reset_password")])
    with tabs[0]:
        with st.form(key="login_form"):
            username = st.text_input(get_text("username"), key="login_username")
            password = st.text_input(get_text("password"), type="password", key="login_password")
            if st.form_submit_button(get_text("login_button")):
                user_id = DatabaseManager.verify_login(username, password)
                if user_id:
                    st.session_state["user_id"] = user_id
                    st.session_state["username"] = username
                    logger.info(f"User {username} logged in successfully")
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    with tabs[1]:
        with st.form(key="register_form"):
            username = st.text_input(get_text("username"), key="register_username")
            password = st.text_input(get_text("password"), type="password", key="register_password")
            sec_question = st.text_input(get_text("sec_question"), key="register_sec_question")
            sec_answer = st.text_input(get_text("sec_answer"), type="password", key="register_sec_answer")
            if st.form_submit_button(get_text("create_account")):
                success, message = DatabaseManager.create_user(username, password, sec_question, sec_answer)
                if success:
                    st.success(message)
                    user_id = DatabaseManager.verify_login(username, password)
                    if user_id:
                        st.session_state["user_id"] = user_id
                        st.session_state["username"] = username
                        logger.info(f"User {username} registered and logged in")
                        st.rerun()
                else:
                    st.error(message)
    with tabs[2]:
        with st.form(key="reset_form"):
            username = st.text_input(get_text("username"), key="reset_username")
            sec_answer = st.text_input(get_text("sec_answer"), type="password", key="reset_sec_answer")
            new_password = st.text_input(get_text("new_password"), type="password", key="reset_new_password")
            if st.form_submit_button(get_text("reset_button")):
                if DatabaseManager.reset_password(username, sec_answer, new_password):
                    st.success("Password reset successfully")
                    logger.info(f"Password reset for user {username}")
                else:
                    st.error("Invalid username or security answer")

def main() -> None:
    """Main application entry point."""
    st.set_page_config(page_title=APP_TITLE_EN, page_icon="🍽️", layout="wide")
    inject_css()
    initialize_session_state()

    lang = st.session_state.get("language", "English")
    st.title(get_text("app_title"))

    if not current_user_id():
        auth_gate_tabs()
    else:
        topbar_account()
        tabs = st.tabs([
            get_text("inventory"),
            get_text("recipes"),
            get_text("feasibility"),
            get_text("shopping_list"),
            get_text("adjust_recipe"),
            get_text("food_timeline")
        ])
        with tabs[0]:
            inventory_page()
        with tabs[1]:
            recipes_page()
        with tabs[2]:
            feasibility_page()
        with tabs[3]:
            shopping_list_page()
        with tabs[4]:
            recipe_adjustment_page()
        with tabs[5]:
            food_timeline_page()

if __name__ == "__main__":
    main()