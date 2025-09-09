



import streamlit as st
import html
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from database import DatabaseManager
from utils import VALID_UNITS, validate_unit
from config import APP_TITLE_EN, APP_TITLE_VI
import logging
from collections import defaultdict, Counter

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# Tiêm CSS tùy chỉnh
def inject_css():
    """Tiêm CSS tùy chỉnh để định dạng ứng dụng Streamlit."""
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
        logger.error(f"Lỗi tiêm CSS: {e}")
        st.error("Không thể áp dụng kiểu dáng tùy chỉnh. Tiếp tục với kiểu mặc định.")

# Văn bản đa ngôn ngữ (i18n)
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
        "cook_failed": "Cooking failed.",
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
        "cook_adjusted_success": "Adjusted recipe '{title}' cooked successfully.",
        "cook_adjusted_failed": "Failed to cook adjusted recipe '{title}'.",
        "not_logged_in": "You must be logged in to access this page.",
        "error_title_required": "Recipe title is required.",
        "error_ingredients_required": "At least one valid ingredient (with name and positive quantity) is required.",
        "duplicate_recipe": "A recipe with this title already exists.",
        "error_invalid_name": "Invalid ingredient name: {name}",
        "error_invalid_unit": "Invalid unit: {unit}",
        "error_negative_qty": "Quantity must be positive for ingredient: {name}",
        "save_success": "Recipe '{title}' saved successfully.",
        "update_success": "Recipe '{title}' updated successfully.",
        "delete_success": "Recipe '{title}' deleted successfully.",
        "save_failed": "Failed to save recipe '{title}': {error}",
        "update_failed": "Failed to update recipe '{title}': {error}",
        "delete_failed": "Failed to delete recipe '{title}'.",
        "deleting": "Deleting recipe '{title}'",
        "db_error": "Database error: {error}",
        "food_timeline": "🍲 Food Timeline",
        "no_history": "No cooking history yet.",
        "no_entries": "No entries match the filters.",
        "congrats": "Congratulations! You have reached {stars} with {dish} 🎉",
        "signature_dish": "Signature Dish",
        "search_placeholder": "Search (e.g., tag:signature, week:1, day:2025-09-01)",
        "reset_filter": "🔄 Reset filter",
        "stats_week": "This week you cooked {count} dishes, most frequent: {dish}",
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
        "category": "Thể loại",
        "instructions": "Hướng dẫn",
        "servings": "Khẩu phần",
        "name": "Tên",
        "quantity": "Số lượng",
        "unit": "Đơn vị",
        "need": "Cần",
        "have": "Có",
        "missing": "Thiếu",
        "inventory": "📦 Kho hàng",
        "your_stock": "Kho của bạn",
        "no_ingredients": "Chưa có nguyên liệu.",
        "unit_tips": "Mẹo đơn vị: sử dụng g, kg, ml, l, tsp, tbsp, cup, piece, cái, pcs, lạng, chén, bát.",
        "add_ingredient": "Thêm nguyên liệu mới",
        "recipes": "📖 Công thức",
        "your_recipes": "Công thức của bạn",
        "no_recipes": "Chưa có công thức.",
        "save_recipe": "Lưu công thức",
        "update_recipe": "Cập nhật công thức",
        "delete_recipe": "Xóa công thức",
        "feasibility": "✅ Tính khả thi & Mua sắm",
        "create_recipes_first": "Hãy tạo công thức trước.",
        "you_can_cook": "Tính khả thi công thức và Danh sách mua sắm",
        "none_yet": "Chưa có.",
        "all_available": "Tất cả nguyên liệu đều có sẵn.",
        "cook": "Nấu ăn",
        "missing_something": "Thiếu nguyên liệu",
        "all_feasible": "Tất cả công thức đều khả thi 🎉",
        "add_to_shopping": "Thêm nguyên liệu thiếu vào Danh sách mua sắm",
        "shopping_list": "🛒 Danh sách mua sắm",
        "empty_list": "Danh sách mua sắm của bạn trống.",
        "update_inventory": "Cập nhật kho từ Danh sách mua sắm",
        "purchased": "Kho hàng đã được cập nhật với các mặt hàng đã mua.",
        "select_recipes_label": "Chọn các công thức để xử lý",
        "select_purchased": "Chọn mục đã mua",
        "sent_to_shopping": "Đã thêm nguyên liệu thiếu vào danh sách mua sắm.",
        "cook_success": "Nấu ăn thành công.",
        "cook_failed": "Nấu ăn thất bại.",
        "adjust_recipe": "⚖️ Điều chỉnh Công thức",
        "select_recipe": "Chọn Công thức",
        "adjustment_type": "Loại Điều chỉnh",
        "by_servings": "Theo Khẩu phần",
        "by_main_ingredient": "Theo Nguyên liệu Chính",
        "new_servings": "Khẩu phần Mới",
        "main_ingredient": "Nguyên liệu Chính",
        "new_quantity": "Số lượng Mới",
        "spice_level": "Mức Độ Gia vị",
        "mild": "Nhẹ (60%)",
        "normal": "Bình thường (80%)",
        "rich": "Đậm (100%)",
        "adjusted_recipe": "Công thức Đã Điều chỉnh",
        "cook_adjusted": "Nấu Công thức Đã Điều chỉnh",
        "add_to_shopping_adjusted": "Thêm Nguyên liệu Thiếu vào Danh sách Mua sắm",
        "adjusted_recipe_title": "Đã điều chỉnh: {title}",
        "no_recipe_selected": "Vui lòng chọn một công thức để điều chỉnh.",
        "invalid_adjustment": "Tham số điều chỉnh không hợp lệ.",
        "cook_adjusted_success": "Công thức đã điều chỉnh '{title}' được nấu thành công.",
        "cook_adjusted_failed": "Không thể nấu công thức đã điều chỉnh '{title}'.",
        "not_logged_in": "Bạn phải đăng nhập để truy cập trang này.",
        "error_title_required": "Tiêu đề công thức là bắt buộc.",
        "error_ingredients_required": "Cần ít nhất một nguyên liệu hợp lệ (có tên và số lượng dương).",
        "duplicate_recipe": "Công thức với tiêu đề này đã tồn tại.",
        "error_invalid_name": "Tên nguyên liệu không hợp lệ: {name}",
        "error_invalid_unit": "Đơn vị không hợp lệ: {unit}",
        "error_negative_qty": "Số lượng phải dương cho nguyên liệu: {name}",
        "save_success": "Công thức '{title}' được lưu thành công.",
        "update_success": "Công thức '{title}' được cập nhật thành công.",
        "delete_success": "Công thức '{title}' được xóa thành công.",
        "save_failed": "Không thể lưu công thức '{title}': {error}",
        "update_failed": "Không thể cập nhật công thức '{title}': {error}",
        "delete_failed": "Không thể xóa công thức '{title}'.",
        "deleting": "Đang xóa công thức '{title}'",
        "db_error": "Lỗi cơ sở dữ liệu: {error}",
        "food_timeline": "🍲 Dòng thời gian món đã nấu",
        "no_history": "Chưa có lịch sử nấu ăn.",
        "no_entries": "Không có mục nào phù hợp với bộ lọc.",
        "congrats": "Chúc mừng! Bạn đã lên {stars} với {dish} 🎉",
        "signature_dish": "Món tủ",
        "search_placeholder": "Tìm kiếm (ví dụ: tag:món tủ, tuần:1, ngày:2025-09-01)",
        "reset_filter": "🔄 Xóa bộ lọc",
        "stats_week": "Tuần này bạn nấu {count} món, nhiều nhất là {dish}",
    }
}

# Trợ giúp i18n
def get_text(key: str, **kwargs) -> str:
    """Truy cập an toàn i18n: Định dạng văn bản nếu có kwargs, quay lại key nếu không tìm thấy."""
    lang = st.session_state.get("language", "English")
    template = TEXT.get(lang, {}).get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, ValueError) as e:
            logger.warning(f"i18n format error for key='{key}' in lang='{lang}': {e}")
            return template
    return template

# Quản lý trạng thái phiên
def initialize_session_state():
    """Khởi tạo giá trị mặc định cho trạng thái phiên."""
    defaults = {
        "language": "English",
        "user_id": None,
        "username": None,
        "editing_recipe_id": None,
        "recipe_form_data": {
            "title": "",
            "category": "",
            "instructions": "",
            "is_signature": False,
            "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
        },
        "shopping_list_data": [],
        "adjusted_recipe": None,
        "search_value": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def current_user_id() -> Optional[int]:
    """Lấy ID người dùng hiện tại từ trạng thái phiên."""
    user_id = st.session_state.get("user_id")
    return user_id if isinstance(user_id, int) else None

def topbar_account():
    """Hiển thị thanh trên cùng với tên người dùng, chọn ngôn ngữ và nút đăng xuất."""
    user_id = current_user_id()
    if not user_id:
        return
    with st.container():
        st.markdown('<div id="topbar-account">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            username = st.session_state.get('username', 'Unknown')
            st.write(f"{get_text('username')}: {html.escape(username)}")
        with col2:
            lang_index = 0 if st.session_state.get("language", "English") == "English" else 1
            st.selectbox(
                get_text("language"),
                ["English", "Vietnamese"],
                index=lang_index,
                key="language_selector",
                on_change=lambda: st.session_state.update({"language": st.session_state.language_selector})
            )
        with col3:
            if st.button(get_text("logout"), key="logout_btn"):
                st.session_state.clear()
                initialize_session_state()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Tính điểm sao
def calculate_stars(count: int, is_signature: bool) -> int:
    """Tính điểm sao dựa trên số lần nấu và trạng thái món tủ."""
    if not isinstance(count, int) or count < 0:
        return 0
    thresholds = [(15, 5), (8, 4), (5, 3), (3, 2), (1, 1)]
    return 5 if is_signature else next((stars for threshold, stars in thresholds if count >= threshold), 0)

# Quản lý Kho hàng
def inventory_page():
    """Hiển thị và quản lý kho nguyên liệu của người dùng."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return

    inventory_key = f"inventory_data_{user_id}"
    try:
        inventory = DatabaseManager.list_inventory(user_id)
        if not isinstance(inventory, list):
            raise ValueError("list_inventory did not return a list")
        st.session_state[inventory_key] = inventory
    except Exception as e:
        logger.error(f"Lỗi tải kho cho user_id={user_id}: {e}")
        st.error(get_text("db_error").format(error=e))
        st.session_state[inventory_key] = []
        return

    st.header(get_text("inventory"))
    st.subheader(get_text("your_stock"))
    st.caption(get_text("unit_tips"))

    # Form thêm nguyên liệu mới
    with st.expander(get_text("add_ingredient")):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            ingredient_name = st.text_input(get_text("name"), placeholder=get_text("e.g., chicken"), key="new_ingredient_name")
        with col2:
            quantity = st.number_input(get_text("quantity"), min_value=0.0, step=0.1, value=0.0, key="new_quantity")
        with col3:
            unit = st.selectbox(get_text("unit"), options=VALID_UNITS, key="new_unit")
        if st.button(get_text("add_ingredient"), key="add_ingredient_btn"):
            if not ingredient_name.strip() or quantity < 0 or not unit:
                st.error(get_text("error_ingredients_required"))
                return
            if not DatabaseManager.validate_name(ingredient_name):
                st.error(get_text("error_invalid_name").format(name=ingredient_name))
                return
            if not validate_unit(unit):
                st.error(get_text("error_invalid_unit").format(unit=unit))
                return
            try:
                result = DatabaseManager.upsert_inventory(user_id, ingredient_name.strip(), quantity, unit)
                if not isinstance(result, tuple) or len(result) != 2:
                    raise ValueError("upsert_inventory did not return a tuple (success, msg)")
                success, msg = result
                if success:
                    st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            except Exception as e:
                logger.error(f"Lỗi thêm nguyên liệu {ingredient_name}: {e}")
                st.error(get_text("db_error").format(error=e))

    # Hiển thị và chỉnh sửa kho hiện tại
    if st.session_state[inventory_key]:
        edited_data = st.data_editor(
            st.session_state[inventory_key],
            column_config={
                "id": None,
                "name": st.column_config.TextColumn(get_text("name"), required=True),
                "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
                "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
            },
            num_rows="dynamic",
            key=f"inventory_editor_{user_id}",
            hide_index=True
        )
        # Detect changes
        original_ids = {item["id"] for item in st.session_state[inventory_key] if "id" in item}
        edited_ids = {item["id"] for item in edited_data if "id" in item}
        deleted_ids = original_ids - edited_ids

        for item in edited_data:
            if not item.get("name") or item.get("quantity") is None or not item.get("unit"):
                st.error(get_text("error_ingredients_required"))
                continue
            if not DatabaseManager.validate_name(item["name"]):
                st.error(get_text("error_invalid_name").format(name=item["name"]))
                continue
            if not validate_unit(item["unit"]):
                st.error(get_text("error_invalid_unit").format(unit=item["unit"]))
                continue
            if item["quantity"] < 0:
                st.error(get_text("error_negative_qty").format(name=item["name"]))
                continue
            try:
                result = DatabaseManager.upsert_inventory(user_id, item["name"].strip(), item["quantity"], item["unit"])
                if not isinstance(result, tuple) or len(result) != 2:
                    raise ValueError("upsert_inventory did not return a tuple (success, msg)")
                success, msg = result
                if not success:
                    st.error(msg)
            except Exception as e:
                logger.error(f"Lỗi cập nhật kho cho {item['name']}: {e}")
                st.error(get_text("db_error").format(error=e))

        for item_id in deleted_ids:
            try:
                result = DatabaseManager.delete_inventory(item_id)
                if not isinstance(result, tuple) or len(result) != 2:
                    raise ValueError("delete_inventory did not return a tuple (success, msg)")
                success, msg = result
                if not success:
                    st.error(msg)
            except Exception as e:
                logger.error(f"Lỗi xóa mục kho {item_id}: {e}")
                st.error(get_text("db_error").format(error=e))

        # Reload if changes detected
        if edited_data != st.session_state[inventory_key] or deleted_ids:
            try:
                st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
            except Exception as e:
                logger.error(f"Lỗi reload kho: {e}")
                st.session_state[inventory_key] = []
            st.rerun()
    else:
        st.info(get_text("no_ingredients"))

# Quản lý Công thức
def recipes_page():
    """Hiển thị và quản lý công thức của người dùng."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return

    if "recipe_form_data" not in st.session_state:
        st.session_state.recipe_form_data = {
            "title": "",
            "category": "",
            "instructions": "",
            "is_signature": False,
            "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
        }

    try:
        recipes = DatabaseManager.list_recipes(user_id)
        if not isinstance(recipes, list):
            raise ValueError("list_recipes did not return a list")
    except Exception as e:
        logger.error(f"Lỗi tải công thức cho user_id={user_id}: {e}")
        st.error(get_text("db_error").format(error=e))
        recipes = []
        return

    st.header(get_text("recipes"))
    st.subheader(get_text("your_recipes"))
    st.caption(get_text("unit_tips"))

    if not recipes:
        st.info(get_text("no_recipes"))

    form_data = st.session_state.recipe_form_data
    recipe_id = st.session_state.get("editing_recipe_id")

    with st.form(key="recipe_form"):
        title = st.text_input(get_text("title"), value=form_data["title"], key="recipe_title", max_chars=200)
        category = st.text_input(get_text("category"), value=form_data["category"], key="recipe_category", max_chars=50)
        instructions = st.text_area(get_text("instructions"), value=form_data["instructions"], key="recipe_instructions")
        is_signature = st.checkbox(get_text("signature_dish"), value=form_data["is_signature"], key="recipe_is_signature")
        ingredients_data = st.data_editor(
            form_data["ingredients"],
            column_config={
                "name": st.column_config.TextColumn(get_text("name"), required=True, max_chars=100),
                "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
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

            valid_ingredients = [
                ing for ing in ingredients_data
                if DatabaseManager.normalize_name(ing.get("name", "")).strip() and
                isinstance(ing.get("quantity"), (int, float)) and ing["quantity"] > 0 and
                validate_unit(ing.get("unit", ""))
            ]
            if not valid_ingredients:
                st.error(get_text("error_ingredients_required"))
                return

            existing_recipe = next((r for r in recipes if r.get("title") == title.strip() and r.get("id") != recipe_id), None)
            if existing_recipe:
                st.error(get_text("duplicate_recipe"))
                return

            for ing in valid_ingredients:
                if not DatabaseManager.validate_name(ing["name"]):
                    st.error(get_text("error_invalid_name").format(name=ing["name"]))
                    return
                if not validate_unit(ing["unit"]):
                    st.error(get_text("error_invalid_unit").format(unit=ing["unit"]))
                    return
                if ing["quantity"] <= 0:
                    st.error(get_text("error_negative_qty").format(name=ing["name"]))
                    return

            try:
                result = DatabaseManager.create_recipe(
                    user_id, title.strip(), category.strip(), instructions.strip(), valid_ingredients, recipe_id, is_signature
                )
                if not isinstance(result, tuple) or len(result) != 2:
                    raise ValueError("create_recipe did not return a tuple (success, msg)")
                success, msg = result
                if success:
                    st.success(get_text("save_success" if recipe_id is None else "update_success").format(title=title))
                    st.session_state.recipe_form_data = {
                        "title": "",
                        "category": "",
                        "instructions": "",
                        "is_signature": False,
                        "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
                    }
                    st.session_state.editing_recipe_id = None
                    st.rerun()
                else:
                    st.error(get_text("save_failed" if recipe_id is None else "update_failed").format(title=title, error=msg))
            except Exception as e:
                logger.error(f"Lỗi lưu/cập nhật công thức {title}: {e}")
                st.error(get_text("db_error").format(error=e))

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
                            "ingredients": recipe.get("ingredients", [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}])
                        }
                        st.rerun()
                with col2:
                    if st.button(get_text("delete_recipe"), key=f"delete_{recipe.get('id')}"):
                        st.warning(get_text("deleting").format(title=recipe["title"]))
                        try:
                            result = DatabaseManager.delete_recipe(recipe["id"])
                            if not isinstance(result, tuple) or len(result) != 2:
                                raise ValueError("delete_recipe did not return a tuple (success, msg)")
                            success, msg = result
                            if success:
                                st.success(get_text("delete_success").format(title=recipe["title"]))
                                st.rerun()
                            else:
                                st.error(get_text("delete_failed").format(title=recipe["title"]))
                        except Exception as e:
                            logger.error(f"Lỗi xóa công thức {recipe['title']}: {e}")
                            st.error(get_text("db_error").format(error=e))

# Trợ giúp Tính khả thi
def _norm_name(name: str) -> str:
    """Chuẩn hóa tên nguyên liệu để so sánh."""
    return DatabaseManager.normalize_name(name or "").strip().lower()

def _norm_unit(unit: str) -> str:
    """Chuẩn hóa đơn vị để so sánh."""
    return (unit or "").strip().lower()

def _inventory_map(user_id: int) -> Dict[Tuple[str, str], dict]:
    """Tạo bản đồ kho dựa trên tên và đơn vị chuẩn hóa."""
    try:
        inventory = DatabaseManager.list_inventory(user_id)
        if not isinstance(inventory, list):
            raise ValueError("list_inventory did not return a list")
        return {
            (_norm_name(item["name"]), _norm_unit(item["unit"])): item
            for item in inventory
            if item.get("name") and item.get("unit")
        }
    except Exception as e:
        logger.error(f"Lỗi tạo inventory map cho user_id={user_id}: {e}")
        return {}

def recipe_feasibility(recipe: dict, user_id: int) -> Tuple[bool, List[dict]]:
    """Kiểm tra tính khả thi của công thức dựa trên kho. Trả về (feasible: bool, shorts: List[dict])."""
    inv_map = _inventory_map(user_id)
    shorts = []
    feasible = True
    for ing in recipe.get("ingredients", []):
        name = _norm_name(ing.get("name", ""))
        unit = _norm_unit(ing.get("unit", ""))
        qty = float(ing.get("quantity", 0.0))
        if not name or not unit or qty <= 0:
            continue
        key = (name, unit)
        have_qty = float(inv_map.get(key, {}).get("quantity", 0.0))
        missing = max(0.0, qty - have_qty)
        if missing > 1e-9:
            feasible = False
            shorts.append({
                "name": ing.get("name", ""),
                "needed_qty": qty,
                "have_qty": have_qty,
                "needed_unit": unit,
                "have_unit": unit if key in inv_map else "",
                "missing_qty_disp": missing,
                "missing_unit_disp": unit
            })
    return feasible, shorts

def consume_ingredients_for_recipe(recipe: dict, user_id: int) -> bool:
    """Tiêu thụ nguyên liệu từ kho nếu công thức khả thi."""
    inv_map = _inventory_map(user_id)
    feasible, _ = recipe_feasibility(recipe, user_id)
    if not feasible:
        return False
    for ing in recipe.get("ingredients", []):
        name = _norm_name(ing.get("name", ""))
        unit = _norm_unit(ing.get("unit", ""))
        qty = float(ing.get("quantity", 0.0))
        if not name or not unit or qty <= 0:
            continue
        key = (name, unit)
        inv_item = inv_map.get(key)
        if inv_item:
            new_qty = max(0.0, float(inv_item.get("quantity", 0.0)) - qty)
            try:
                result = DatabaseManager.update_inventory_item(inv_item["id"], inv_item["name"], new_qty, inv_item["unit"])
                if not isinstance(result, tuple) or len(result) != 2:
                    raise ValueError("update_inventory_item did not return a tuple (success, msg)")
                success, msg = result
                if not success:
                    logger.error(f"Lỗi cập nhật khi tiêu thụ {name}: {msg}")
                    return False
            except Exception as e:
                logger.error(f"Lỗi cập nhật khi tiêu thụ {name}: {e}")
                return False
    return True

# Trang Tính khả thi
def feasibility_page():
    """Hiển thị tính khả thi của công thức và tùy chọn danh sách mua sắm."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return

    inventory_key = f"inventory_data_{user_id}"
    try:
        recipes = DatabaseManager.list_recipes(user_id)
        if not isinstance(recipes, list):
            raise ValueError("list_recipes did not return a list")
        inventory = DatabaseManager.list_inventory(user_id)
        if not isinstance(inventory, list):
            raise ValueError("list_inventory did not return a list")
        st.session_state[inventory_key] = inventory
    except Exception as e:
        logger.error(f"Lỗi tải dữ liệu cho user_id={user_id}: {e}")
        st.error(get_text("db_error").format(error=e))
        recipes = []
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
        key="recipe_select"
    )

    selected_missing = []
    for result in [r for r in recipe_results if r["recipe"]["title"] in selected_titles]:
        st.markdown(f"#### {html.escape(result['recipe'].get('title', 'Untitled'))}")
        if result["feasible"]:
            st.success(get_text("all_available"))
            if st.button(get_text("cook"), key=f"cook_{result['recipe'].get('id')}"):
                if consume_ingredients_for_recipe(result["recipe"], user_id):
                    try:
                        result_log = DatabaseManager.log_cooked_recipe(user_id, result["recipe"]["id"])
                        if not isinstance(result_log, tuple) or len(result_log) != 2:
                            raise ValueError("log_cooked_recipe did not return a tuple (success, msg)")
                        success, msg = result_log
                        if success:
                            count_result = DatabaseManager.get_cooked_count(user_id, result["recipe"]["id"])
                            if not isinstance(count_result, int):
                                raise ValueError("get_cooked_count did not return an int")
                            count = count_result + 1
                            stars = calculate_stars(count, result["recipe"].get("is_signature", False))
                            if stars > calculate_stars(count - 1, result["recipe"].get("is_signature", False)):
                                st.success(get_text("congrats").format(stars="⭐" * stars, dish=result["recipe"]["title"]))
                            st.success(get_text("cook_success"))
                            st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                            st.rerun()
                        else:
                            st.error(get_text("cook_failed"))
                    except Exception as e:
                        logger.error(f"Lỗi ghi log nấu ăn cho recipe_id={result['recipe']['id']}: {e}")
                        st.error(get_text("db_error").format(error=e))
                else:
                    st.error(get_text("cook_failed"))
                    _, shorts = recipe_feasibility(result["recipe"], user_id)
                    if shorts:
                        st.table([
                            {"Tên (Name)": s["name"], "Cần (Needed)": f"{s['needed_qty']} {s['needed_unit']}",
                             "Có (Available)": f"{s['have_qty']} {s['have_unit']}",
                             "Thiếu (Missing)": f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
                            for s in shorts
                        ])
        else:
            st.warning(get_text("missing_something"))
            st.table([
                {get_text("name"): s["name"], get_text("need"): s["needed_qty"], get_text("have"): s["have_qty"],
                 get_text("unit"): s["needed_unit"], get_text("missing"): s["missing_qty_disp"]}
                for s in result["shorts"]
            ])
            selected_missing.extend(result["shorts"])

    if selected_missing and st.button(get_text("add_to_shopping"), key="add_to_shopping"):
        agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
        for s in selected_missing:
            key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
            agg_missing[key]["name"] = s["name"]
            agg_missing[key]["quantity"] += s["missing_qty_disp"]
            agg_missing[key]["unit"] = s["missing_unit_disp"]
        st.session_state["shopping_list_data"] = list(agg_missing.values())
        st.success(get_text("sent_to_shopping"))
        st.rerun()

# Trang Danh sách mua sắm
def shopping_list_page():
    """Quản lý danh sách mua sắm và cập nhật kho."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return

    inventory_key = f"inventory_data_{user_id}"
    try:
        inventory = DatabaseManager.list_inventory(user_id)
        if not isinstance(inventory, list):
            raise ValueError("list_inventory did not return a list")
        st.session_state[inventory_key] = inventory
    except Exception as e:
        logger.error(f"Lỗi tải kho cho user_id={user_id}: {e}")
        st.error(get_text("db_error").format(error=e))
        st.session_state[inventory_key] = []
        return

    inventory_dict = {_norm_name(ing["name"]): ing for ing in st.session_state[inventory_key] if ing.get("name") and ing.get("unit")}
    shopping_list = st.session_state.get("shopping_list_data", [])

    st.header(get_text("shopping_list"))
    if not shopping_list:
        st.info(get_text("empty_list"))
        return

    # Validate and sanitize shopping_list data
    valid_shopping_list = []
    for item in shopping_list:
        if (
            isinstance(item, dict) and
            item.get("name") and isinstance(item.get("name"), str) and
            DatabaseManager.validate_name(item["name"]) and
            isinstance(item.get("quantity"), (int, float)) and item["quantity"] >= 0 and
            item.get("unit") and validate_unit(item["unit"])
        ):
            valid_shopping_list.append(item)
        else:
            logger.warning(f"Invalid shopping list item: {item}")
    shopping_list = valid_shopping_list
    st.session_state["shopping_list_data"] = shopping_list

    if shopping_list:
        shopping_data = st.data_editor(
            shopping_list,
            column_config={
                "name": st.column_config.TextColumn(get_text("name"), required=True, max_chars=100),
                "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
                "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
            },
            num_rows="dynamic",
            key="shopping_list_editor",
            hide_index=True
        )

        # Update shopping_list_data with edited data
        st.session_state["shopping_list_data"] = shopping_data

        purchased_labels = [f"{item['name']} ({item['unit']})" for item in shopping_data if item.get("name") and item.get("unit")]
        purchased_names = st.multiselect(get_text("select_purchased"), options=purchased_labels, key="purchased_select")

        if st.button(get_text("update_inventory"), key="update_inventory"):
            try:
                for item in shopping_data:
                    item_label = f"{item['name']} ({item['unit']})"
                    if item_label in purchased_names:
                        inv_item = inventory_dict.get(_norm_name(item["name"]))
                        try:
                            if inv_item:
                                new_qty = (inv_item.get("quantity", 0.0) or 0.0) + item.get("quantity", 0.0)
                                result = DatabaseManager.update_inventory_item(inv_item["id"], inv_item["name"], new_qty, inv_item["unit"])
                            else:
                                result = DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"])
                            if not isinstance(result, tuple) or len(result) != 2:
                                raise ValueError("update/upsert_inventory did not return a tuple (success, msg)")
                            success, msg = result
                            if not success:
                                st.error(msg)
                        except Exception as e:
                            logger.error(f"Lỗi cập nhật kho cho {item['name']}: {e}")
                            st.error(get_text("db_error").format(error=e))
                            return
                st.session_state["shopping_list_data"] = [
                    item for item in shopping_data if f"{item['name']} ({item['unit']})" not in purchased_names
                ]
                st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                st.success(get_text("purchased"))
                st.rerun()
            except Exception as e:
                logger.error(f"Lỗi cập nhật kho từ danh sách mua sắm: {e}")
                st.error(get_text("db_error").format(error=e))
    else:
        st.info(get_text("empty_list"))

# Trang Điều chỉnh Công thức
def recipe_adjustment_page():
    """Điều chỉnh công thức dựa trên khẩu phần hoặc nguyên liệu chính."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return

    inventory_key = f"inventory_data_{user_id}"
    try:
        inventory = DatabaseManager.list_inventory(user_id)
        if not isinstance(inventory, list):
            raise ValueError("list_inventory did not return a list")
        st.session_state[inventory_key] = inventory
    except Exception as e:
        logger.error(f"Lỗi tải kho cho user_id={user_id}: {e}")
        st.error(get_text("db_error").format(error=e))
        return

    st.header(get_text("adjust_recipe"))

    try:
        recipes = DatabaseManager.list_recipes(user_id)
        if not isinstance(recipes, list):
            raise ValueError("list_recipes did not return a list")
    except Exception as e:
        logger.error(f"Lỗi tải công thức cho user_id={user_id}: {e}")
        st.error(get_text("db_error").format(error=e))
        recipes = []
        return

    if not recipes:
        st.info(get_text("no_recipes"))
        return

    selected_recipe_title = st.selectbox(get_text("select_recipe"), [r.get("title") for r in recipes], key="recipe_adjust_select")
    if not selected_recipe_title:
        st.warning(get_text("no_recipe_selected"))
        return

    recipe = next(r for r in recipes if r.get("title") == selected_recipe_title)
    adjustment_type = st.radio(get_text("adjustment_type"), [get_text("by_servings"), get_text("by_main_ingredient")], key="adjustment_type")
    adjustment_ratio = 1.0

    if adjustment_type == get_text("by_servings"):
        base_servings = float(recipe.get("servings", 1.0) or 1.0)
        new_servings = st.number_input(get_text("new_servings"), min_value=0.1, step=0.1, value=base_servings, key="new_servings")
        adjustment_ratio = new_servings / base_servings if base_servings > 0 else 1.0
    else:
        main_ingredients = [ing for ing in recipe.get("ingredients", []) if not ing.get("is_spice")]
        if not main_ingredients:
            st.error(get_text("error_ingredients_required"))
            return
        main_ingredient = st.selectbox(get_text("main_ingredient"), [ing.get("name") for ing in main_ingredients], key="main_ingredient")
        selected_ing = next(ing for ing in main_ingredients if ing.get("name") == main_ingredient)
        base_qty = float(selected_ing.get("quantity", 1.0) or 1.0)
        new_quantity = st.number_input(get_text("new_quantity"), min_value=0.0, step=0.1, value=base_qty, key="new_quantity")
        adjustment_ratio = new_quantity / base_qty if base_qty > 0 else 1.0

    spice_display_to_key = {
        get_text("mild"): "mild",
        get_text("normal"): "normal",
        get_text("rich"): "rich"
    }
    spice_level = st.radio(get_text("spice_level"), [get_text("mild"), get_text("normal"), get_text("rich")], key="spice_level")
    spice_key = spice_display_to_key.get(spice_level, "normal")
    spice_factor = {"mild": 0.6, "normal": 0.8, "rich": 1.0}[spice_key]

    adjusted_recipe = {
        "id": recipe.get("id"),
        "title": get_text("adjusted_recipe_title").format(title=recipe.get("title")),
        "category": recipe.get("category"),
        "instructions": recipe.get("instructions"),
        "servings": (float(recipe.get("servings", 1.0) or 1.0) * adjustment_ratio) if adjustment_type == get_text("by_servings") else recipe.get("servings", 1.0),
        "ingredients": [],
        "origin_id": recipe.get("id"),
        "tag": "adjusted"
    }

    for ing in recipe.get("ingredients", []):
        new_qty = max(0.0, float(ing.get("quantity", 0.0)) * adjustment_ratio * (spice_factor if ing.get("is_spice") else 1.0))
        adjusted_recipe["ingredients"].append({
            "name": ing.get("name"),
            "quantity": new_qty,
            "unit": ing.get("unit"),
            "is_spice": ing.get("is_spice", False)
        })

    st.session_state["adjusted_recipe"] = adjusted_recipe
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

    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("cook_adjusted"), key="cook_adjusted"):
            feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
            if feasible and consume_ingredients_for_recipe(adjusted_recipe, user_id):
                try:
                    result_log = DatabaseManager.log_cooked_recipe(user_id, adjusted_recipe["origin_id"])
                    if not isinstance(result_log, tuple) or len(result_log) != 2:
                        raise ValueError("log_cooked_recipe did not return a tuple (success, msg)")
                    success, msg = result_log
                    if success:
                        count_result = DatabaseManager.get_cooked_count(user_id, adjusted_recipe["origin_id"])
                        if not isinstance(count_result, int):
                            raise ValueError("get_cooked_count did not return an int")
                        count = count_result + 1
                        stars = calculate_stars(count, recipe.get("is_signature", False))
                        if stars > calculate_stars(count - 1, recipe.get("is_signature", False)):
                            st.success(get_text("congrats").format(stars="⭐" * stars, dish=adjusted_recipe["title"]))
                        st.success(get_text("cook_adjusted_success").format(title=adjusted_recipe["title"]))
                        st.session_state.pop("adjusted_recipe", None)
                        st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                        st.rerun()
                    else:
                        st.error(get_text("cook_adjusted_failed").format(title=adjusted_recipe["title"]))
                except Exception as e:
                    logger.error(f"Lỗi ghi log nấu công thức đã điều chỉnh {adjusted_recipe['title']}: {e}")
                    st.error(get_text("db_error").format(error=e))
            else:
                st.error(get_text("cook_adjusted_failed").format(title=adjusted_recipe["title"]))
                if shorts:
                    st.table([
                        {"Tên (Name)": s["name"], "Cần (Needed)": f"{s['needed_qty']} {s['needed_unit']}",
                         "Có (Available)": f"{s['have_qty']} {s['have_unit']}",
                         "Thiếu (Missing)": f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
                        for s in shorts
                    ])

    with col2:
        if st.button(get_text("add_to_shopping_adjusted"), key="add_to_shopping_adjusted"):
            feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
            if not feasible:
                agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
                for s in shorts:
                    key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
                    agg_missing[key]["name"] = s["name"]
                    agg_missing[key]["quantity"] += s["missing_qty_disp"]
                    agg_missing[key]["unit"] = s["missing_unit_disp"]
                st.session_state["shopping_list_data"] = st.session_state.get("shopping_list_data", []) + list(agg_missing.values())
                st.success(get_text("sent_to_shopping"))
                st.rerun()

# Trang Dòng thời gian món ăn
def food_timeline_page():
    """Hiển thị lịch sử nấu ăn dưới dạng dòng thời gian với giao diện thẻ."""
    user_id = current_user_id()
    if not user_id:
        st.error(get_text("not_logged_in"))
        return

    inventory_key = f"inventory_data_{user_id}"
    try:
        history = DatabaseManager.list_cooked_history(user_id)
        if not isinstance(history, list):
            raise ValueError("list_cooked_history did not return a list")
        recipes = {r["id"]: r for r in DatabaseManager.list_recipes(user_id)}
        st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
    except Exception as e:
        logger.error(f"Lỗi tải dữ liệu dòng thời gian cho user_id={user_id}: {e}")
        st.error(get_text("db_error").format(error=e))
        history = []
        recipes = {}
        return

    st.header(get_text("food_timeline"))
    if not history:
        st.info(get_text("no_history"))
        return

    recipe_counts = defaultdict(int)
    for h in history:
        recipe_counts[h["recipe_id"]] += 1

    enriched = [
        {
            "date": h["cooked_date"],
            "name": recipes.get(h["recipe_id"], {}).get("title", "Unknown"),
            "stars": calculate_stars(recipe_counts[h["recipe_id"]], recipes.get(h["recipe_id"], {}).get("is_signature", False)),
            "recipe_id": h["recipe_id"],
            "index": idx
        }
        for idx, h in enumerate(history) if h["recipe_id"] in recipes
    ]

    with st.form(key="timeline_search_form"):
        search_query = st.text_input(get_text("search_placeholder"), value=st.session_state.get("search_value", ""), key="timeline_search_input")
        if st.form_submit_button(get_text("reset_filter"), key="reset_filter"):
            st.session_state.search_value = ""
            st.rerun()

    tag_filter, week_filter, day_filter = None, None, None
    if search_query:
        search_query = search_query.strip().lower()
        if search_query.startswith("tag:"):
            tag_filter = search_query[4:].strip()
        elif search_query.startswith(("tuần:", "week:")):
            week_filter = search_query.split(":")[1].strip()
        elif search_query.startswith(("ngày:", "day:")):
            day_filter = search_query.split(":")[1].strip()
        st.session_state.search_value = search_query

    filtered = enriched
    if tag_filter:
        filtered = [e for e in filtered if (tag_filter in ["signature", "món tủ"] and e["stars"] == 5) or (tag_filter == "exploring" and e["stars"] in (1, 2))]
    if week_filter:
        try:
            week_num = int(week_filter)
            start_week = datetime.now() - timedelta(weeks=week_num - 1, days=datetime.now().weekday())
            end_week = start_week + timedelta(days=6)
            filtered = [e for e in filtered if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]
        except ValueError:
            pass
    if day_filter:
        try:
            day_date = datetime.strptime(day_filter, "%Y-%m-%d").date()
            filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date() == day_date]
        except ValueError:
            pass
    if search_query and not any([tag_filter, week_filter, day_filter]):
        filtered = [e for e in filtered if search_query.lower() in e["name"].lower()]

    if not filtered:
        st.info(get_text("no_entries"))
        return

    filtered.sort(key=lambda e: e["date"], reverse=True)
    current_date = datetime.now()
    start_week = current_date - timedelta(days=current_date.weekday())
    end_week = start_week + timedelta(days=6)
    week_history = [e for e in enriched if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]

    if week_history:
        count = len(week_history)
        most_dish = Counter(e["name"] for e in week_history).most_common(1)[0][0] if week_history else "None"
        st.info(get_text("stats_week").format(count=count, dish=most_dish))

    groups = defaultdict(list)
    for e in filtered:
        groups[datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date()].append(e)

    for day in sorted(groups.keys(), reverse=True):
        with st.container():
            st.markdown('<div class="food-card">', unsafe_allow_html=True)
            st.subheader(day.strftime("%Y-%m-%d"))
            for e in groups[day]:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"<span class='dish-name'>{html.escape(e['name'])}</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<span class='stars'>{'⭐' * e['stars']}</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# Trang Xác thực
def auth_gate_tabs():
    """Hiển thị các tab xác thực cho đăng nhập, đăng ký và đặt lại mật khẩu."""
    tabs = st.tabs([get_text("login"), get_text("register"), get_text("reset_password")])
    with tabs[0]:
        username = st.text_input(get_text("username"), key="login_username", max_chars=50)
        password = st.text_input(get_text("password"), type="password", key="login_password")
        if st.button(get_text("login_button"), key="login_btn"):
            if not username.strip() or not password.strip():
                st.error(get_text("error_ingredients_required"))
                return
            try:
                result = DatabaseManager.verify_login(username, password)
                if not isinstance(result, tuple) or len(result) != 2:
                    raise ValueError("verify_login did not return a tuple (success, result)")
                success, result = result
                if success:
                    st.session_state.update(user_id=result, username=username.strip())
                    st.success(get_text("login_button") + " thành công!")
                    st.rerun()
                else:
                    st.error(result)
            except Exception as e:
                logger.error(f"Lỗi đăng nhập cho username={username}: {e}")
                st.error(get_text("db_error").format(error=e))
    with tabs[1]:
        username = st.text_input(get_text("username"), key="register_username", max_chars=50, help=get_text("unit_tips"))
        password = st.text_input(get_text("password"), type="password", key="register_password", help="Tối thiểu 8 ký tự, có chữ, số, ký tự đặc biệt")
        sec_question = st.text_input(get_text("sec_question"), key="sec_question", max_chars=200, value="tai khoan")
        sec_answer = st.text_input(get_text("sec_answer"), type="password", key="sec_answer", max_chars=100, value="test")
        if st.button(get_text("create_account"), key="register_btn"):
            if not all([username.strip(), password.strip(), sec_question.strip(), sec_answer.strip()]):
                st.error(get_text("error_ingredients_required"))
                return
            try:
                result = DatabaseManager.create_user(username, password, sec_question, sec_answer)
                if not isinstance(result, tuple) or len(result) != 2:
                    raise ValueError("create_user did not return a tuple (success, message)")
                success, message = result
                if success:
                    st.success(message)
                    login_result = DatabaseManager.verify_login(username, password)
                    if not isinstance(login_result, tuple) or len(login_result) != 2:
                        raise ValueError("verify_login did not return a tuple (success, result)")
                    login_success, login_id = login_result
                    if login_success:
                        st.session_state.update(user_id=login_id, username=username.strip())
                        st.rerun()
                    else:
                        st.error(login_id)
                else:
                    st.error(message)
            except Exception as e:
                logger.error(f"Lỗi đăng ký cho username={username}: {e}")
                st.error(get_text("db_error").format(error=e))
    with tabs[2]:
        username = st.text_input(get_text("username"), key="reset_username", max_chars=50)
        sec_answer = st.text_input(get_text("sec_answer"), type="password", key="reset_sec_answer", max_chars=100)
        new_password = st.text_input(get_text("new_password"), type="password", key="new_password")
        if st.button(get_text("reset_button"), key="reset_btn"):
            if not all([username.strip(), sec_answer.strip(), new_password.strip()]):
                st.error(get_text("error_ingredients_required"))
                return
            try:
                result = DatabaseManager.reset_password(username, sec_answer, new_password)
                if not isinstance(result, tuple) or len(result) != 2:
                    raise ValueError("reset_password did not return a tuple (success, message)")
                success, message = result
                if success:
                    st.success(message)
                else:
                    st.error(message)
            except Exception as e:
                logger.error(f"Lỗi đặt lại mật khẩu cho username={username}: {e}")
                st.error(get_text("db_error").format(error=e))

# Hàm chính
def main():
    """Điểm vào ứng dụng chính."""
    try:
        initialize_session_state()
        inject_css()
        st.title(get_text("app_title"))
        if current_user_id():
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
        else:
            auth_gate_tabs()
    except Exception as e:
        logger.error(f"Lỗi trong hàm main: {e}")
        st.error("Đã xảy ra lỗi không mong muốn. Vui lòng làm mới trang hoặc liên hệ hỗ trợ.")

if __name__ == "__main__":
    main()