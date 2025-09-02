# ui.py
import streamlit as st
import html
from datetime import datetime, timedelta, date
import csv
import io
from typing import Optional
from database import DatabaseManager
from utils import validate_unit
from config import APP_TITLE_EN, APP_TITLE_VI, VALID_UNITS
import logging
from collections import defaultdict, Counter
from business_logic import recipe_feasibility, consume_ingredients_for_recipe

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def inject_css():
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
        "inventory": "📦 Inventory",
        "your_stock": "Your Stock",
        "no_ingredients": "No ingredients yet.",
        "add_ingredient": "Add Ingredient",
        "update_ingredient": "Update",
        "delete_ingredient": "Delete",
        "recipes": "📖 Recipes",
        "your_recipes": "Your Recipes",
        "no_recipes": "No recipes yet.",
        "create_recipe": "Create Recipe",
        "edit_recipe": "Edit Recipe",
        "delete_recipe": "Delete",
        "feasibility": "✅ Feasibility & Shopping",
        "create_recipes_first": "Create recipes first to check feasibility.",
        "feasible": "Feasible",
        "not_feasible": "Not Feasible: Missing Ingredients",
        "add_to_shopping": "Add to Shopping List",
        "cook_recipe": "Cook Recipe",
        "shopping_list": "🛒 Shopping List",
        "no_shopping_items": "No items in shopping list.",
        "add_to_inventory": "Add to Inventory",
        "clear_shopping_list": "Clear Shopping List",
        "adjust_recipe": "🔧 Adjust Recipe",
        "select_recipe": "Select a recipe",
        "adjust_servings": "Adjust Servings",
        "food_timeline": "📅 Food Timeline",
        "no_history": "No cooking history yet.",
        "stats_week": "This week: {count} dishes cooked, most frequent: {dish}",
        "db_error": "Database error: {error}",
        "invalid_unit": "Invalid unit: {unit}",
        "recipe_saved": "Recipe saved successfully",
        "recipe_deleted": "Recipe deleted successfully",
        "inventory_updated": "Inventory updated successfully",
        "inventory_deleted": "Ingredient deleted successfully",
        "recipe_cooked": "Recipe cooked successfully",
    },
    "Vietnamese": {
        "app_title": APP_TITLE_VI,
        "login": "🔐 Đăng Nhập",
        "username": "Tên Người Dùng",
        "password": "Mật Khẩu",
        "login_button": "Đăng Nhập",
        "register": "🆕 Đăng Ký",
        "sec_question": "Câu Hỏi Bảo Mật (để đặt lại mật khẩu)",
        "sec_answer": "Câu Trả Lời Bảo Mật",
        "create_account": "Tạo Tài Khoản",
        "reset_password": "♻️ Đặt Lại Mật Khẩu",
        "new_password": "Mật Khẩu Mới",
        "reset_button": "Đặt Lại Mật Khẩu",
        "inventory": "📦 Kho",
        "your_stock": "Kho Của Bạn",
        "no_ingredients": "Chưa có nguyên liệu.",
        "add_ingredient": "Thêm Nguyên Liệu",
        "update_ingredient": "Cập Nhật",
        "delete_ingredient": "Xóa",
        "recipes": "📖 Công Thức",
        "your_recipes": "Công Thức Của Bạn",
        "no_recipes": "Chưa có công thức.",
        "create_recipe": "Tạo Công Thức",
        "edit_recipe": "Chỉnh Sửa Công Thức",
        "delete_recipe": "Xóa",
        "feasibility": "✅ Khả Thi & Mua Sắm",
        "create_recipes_first": "Tạo công thức trước để kiểm tra khả thi.",
        "feasible": "Khả Thi",
        "not_feasible": "Không Khả Thi: Thiếu Nguyên Liệu",
        "add_to_shopping": "Thêm vào Danh Sách Mua Sắm",
        "cook_recipe": "Nấu Công Thức",
        "shopping_list": "🛒 Danh Sách Mua Sắm",
        "no_shopping_items": "Chưa có mục nào trong danh sách mua sắm.",
        "add_to_inventory": "Thêm vào Kho",
        "clear_shopping_list": "Xóa Danh Sách Mua Sắm",
        "adjust_recipe": "🔧 Điều Chỉnh Công Thức",
        "select_recipe": "Chọn một công thức",
        "adjust_servings": "Điều Chỉnh Khẩu Phần",
        "food_timeline": "📅 Lịch Sử Ăn Uống",
        "no_history": "Chưa có lịch sử nấu ăn.",
        "stats_week": "Tuần này: {count} món ăn được nấu, phổ biến nhất: {dish}",
        "db_error": "Lỗi cơ sở dữ liệu: {error}",
        "invalid_unit": "Đơn vị không hợp lệ: {unit}",
        "recipe_saved": "Lưu công thức thành công",
        "recipe_deleted": "Xóa công thức thành công",
        "inventory_updated": "Cập nhật kho thành công",
        "inventory_deleted": "Xóa nguyên liệu thành công",
        "recipe_cooked": "Nấu công thức thành công",
    }
}

def get_text(key: str) -> str:
    lang = st.session_state.get("language", "English")
    return TEXT.get(lang, TEXT["English"]).get(key, key)

def topbar_account():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{st.session_state.username}**", unsafe_allow_html=True)
    with col2:
        lang = st.selectbox("Language", ["English", "Vietnamese"], key="language_selector")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

def inventory_page():
    user_id = st.session_state.user_id
    st.subheader(get_text("your_stock"))
    inventory = DatabaseManager.list_inventory(user_id)
    if not inventory:
        st.info(get_text("no_ingredients"))
    else:
        st.table([{"Name": item["name"], "Quantity": f"{item['quantity']} {item['unit']}",
                   "Actions": f"<button onclick='st.session_state.delete_inventory={item['id']};st.rerun()'>Delete</button>"} for item in inventory],
                 unsafe_allow_html=True)
    if "delete_inventory" in st.session_state:
        if DatabaseManager.delete_inventory(st.session_state.delete_inventory):
            st.success(get_text("inventory_deleted"))
        del st.session_state.delete_inventory
        st.rerun()

    with st.form("add_inventory"):
        name = st.text_input(get_text("add_ingredient"))
        quantity = st.number_input("Quantity", min_value=0.0, step=0.01)
        unit = st.selectbox("Unit", VALID_UNITS)
        if st.form_submit_button(get_text("add_ingredient")):
            if not name:
                st.error("Ingredient name is required")
            elif not validate_unit(unit):
                st.error(get_text("invalid_unit").format(unit=unit))
            elif DatabaseManager.upsert_inventory(user_id, name, quantity, unit):
                st.success(get_text("inventory_updated"))
                st.rerun()
            else:
                st.error(get_text("db_error").format(error="Failed to update inventory"))

def recipes_page():
    user_id = st.session_state.user_id
    st.subheader(get_text("your_recipes"))
    recipes = DatabaseManager.list_recipes(user_id)
    if not recipes:
        st.info(get_text("no_recipes"))
    else:
        for recipe in recipes:
            with st.expander(f"{recipe['title']} ({recipe['servings']} servings)"):
                st.write(f"Category: {recipe['category'] or 'None'}")
                st.write(f"Instructions: {recipe['instructions'] or 'None'}")
                st.write("Ingredients:")
                st.table(recipe["ingredients"])
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(get_text("edit_recipe"), key=f"edit_{recipe['id']}"):
                        st.session_state.editing_recipe_id = recipe["id"]
                        st.session_state.recipe_form_data = {
                            "title": recipe["title"],
                            "category": recipe["category"] or "",
                            "instructions": recipe["instructions"] or "",
                            "is_signature": recipe["is_signature"],
                            "ingredients": recipe["ingredients"]
                        }
                        st.rerun()
                with col2:
                    if st.button(get_text("delete_recipe"), key=f"delete_{recipe['id']}"):
                        if DatabaseManager.delete_recipe(recipe["id"]):
                            st.success(get_text("recipe_deleted"))
                            st.rerun()

    with st.form("recipe_form"):
        title = st.text_input(get_text("create_recipe") if not st.session_state.editing_recipe_id else get_text("edit_recipe"))
        category = st.text_input("Category")
        instructions = st.text_area("Instructions")
        servings = st.number_input("Servings", min_value=1, value=1)
        is_signature = st.checkbox("Signature Recipe")
        st.write("Ingredients")
        ingredients = []
        for i in range(st.session_state.recipe_form_data["ingredients"].__len__()):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    name = st.text_input("Name", value=st.session_state.recipe_form_data["ingredients"][i]["name"], key=f"ing_name_{i}")
                with col2:
                    qty = st.number_input("Quantity", min_value=0.0, step=0.01, value=st.session_state.recipe_form_data["ingredients"][i]["quantity"], key=f"ing_qty_{i}")
                with col3:
                    unit = st.selectbox("Unit", VALID_UNITS, index=VALID_UNITS.index(st.session_state.recipe_form_data["ingredients"][i]["unit"]), key=f"ing_unit_{i}")
                with col4:
                    is_spice = st.checkbox("Spice", value=st.session_state.recipe_form_data["ingredients"][i]["is_spice"], key=f"ing_spice_{i}")
                ingredients.append({"name": name, "quantity": qty, "unit": unit, "is_spice": is_spice})
        if st.button("Add Ingredient"):
            st.session_state.recipe_form_data["ingredients"].append({"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False})
            st.rerun()
        if st.form_submit_button(get_text("create_recipe") if not st.session_state.editing_recipe_id else get_text("edit_recipe")):
            success, message = DatabaseManager.create_recipe_from_table(user_id, title, category, instructions, servings, is_signature, ingredients)
            if success:
                st.success(get_text("recipe_saved"))
                st.session_state.editing_recipe_id = None
                st.session_state.recipe_form_data = {
                    "title": "", "category": "", "instructions": "", "is_signature": False,
                    "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
                }
                st.rerun()
            else:
                st.error(message)

def feasibility_page():
    user_id = st.session_state.user_id
    recipes = DatabaseManager.list_recipes(user_id)
    if not recipes:
        st.info(get_text("create_recipes_first"))
        return
    recipe_options = {r["title"]: r for r in recipes}
    selected = st.selectbox(get_text("select_recipe"), list(recipe_options.keys()))
    if selected:
        recipe = recipe_options[selected]
        feasible, shorts = recipe_feasibility(recipe, user_id)
        st.write(get_text("feasible") if feasible else get_text("not_feasible"))
        if shorts:
            st.table([{"Name": s["name"], "Needed": f"{s['needed_qty']} {s['needed_unit']}",
                       "Available": f"{s['have_qty']} {s['have_unit']}",
                       "Missing": f"{s['missing_qty_disp']} {s['missing_unit_disp']}"} for s in shorts])
            if st.button(get_text("add_to_shopping")):
                st.session_state.shopping_list_data.extend([{"name": s["name"], "quantity": s["missing_qty_disp"], "unit": s["missing_unit_disp"]} for s in shorts])
                st.rerun()
        if feasible and st.button(get_text("cook_recipe")):
            if consume_ingredients_for_recipe(recipe, user_id):
                st.success(get_text("recipe_cooked"))
                st.rerun()
            else:
                st.error(get_text("db_error").format(error="Failed to cook recipe"))

def shopping_list_page():
    if not st.session_state.shopping_list_data:
        st.info(get_text("no_shopping_items"))
        return
    st.table(st.session_state.shopping_list_data)
    with st.form("add_to_inventory"):
        for i, item in enumerate(st.session_state.shopping_list_data):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(item["name"])
            with col2:
                qty = st.number_input("Quantity", min_value=0.0, step=0.01, value=item["quantity"], key=f"shop_qty_{i}")
                item["quantity"] = qty
            with col3:
                unit = st.selectbox("Unit", VALID_UNITS, index=VALID_UNITS.index(item["unit"]), key=f"shop_unit_{i}")
                item["unit"] = unit
        if st.form_submit_button(get_text("add_to_inventory")):
            user_id = st.session_state.user_id
            success = True
            for item in st.session_state.shopping_list_data:
                if not DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"]):
                    success = False
            if success:
                st.session_state.shopping_list_data = []
                st.success(get_text("inventory_updated"))
                st.rerun()
            else:
                st.error(get_text("db_error").format(error="Failed to update inventory"))
    if st.button(get_text("clear_shopping_list")):
        st.session_state.shopping_list_data = []
        st.rerun()

def recipe_adjustment_page():
    user_id = st.session_state.user_id
    recipes = DatabaseManager.list_recipes(user_id)
    recipe_options = {r["title"]: r for r in recipes}
    selected = st.selectbox(get_text("select_recipe"), list(recipe_options.keys()))
    if selected:
        recipe = recipe_options[selected]
        new_servings = st.number_input(get_text("adjust_servings"), min_value=1, value=recipe["servings"])
        if new_servings != recipe["servings"]:
            factor = new_servings / recipe["servings"]
            adjusted = {"id": recipe["id"], "title": recipe["title"], "servings": new_servings,
                        "ingredients": [{"name": ing["name"], "quantity": ing["quantity"] * factor,
                                         "unit": ing["unit"], "is_spice": ing["is_spice"]} for ing in recipe["ingredients"]]}
            st.session_state.adjusted_recipe = adjusted
            st.table(adjusted["ingredients"])
            feasible, shorts = recipe_feasibility(adjusted, user_id)
            st.write(get_text("feasible") if feasible else get_text("not_feasible"))
            if shorts:
                st.table([{"Name": s["name"], "Needed": f"{s['needed_qty']} {s['needed_unit']}",
                           "Available": f"{s['have_qty']} {s['have_unit']}",
                           "Missing": f"{s['missing_qty_disp']} {s['missing_unit_disp']}"} for s in shorts])
            if feasible and st.button(get_text("cook_recipe")):
                if consume_ingredients_for_recipe(adjusted, user_id):
                    st.success(get_text("recipe_cooked"))
                    st.session_state.adjusted_recipe = None
                    st.rerun()
                else:
                    st.error(get_text("db_error").format(error="Failed to cook recipe"))

def food_timeline_page():
    user_id = st.session_state.user_id
    history = DatabaseManager.list_cooked_history(user_id)
    if not history:
        st.info(get_text("no_history"))
        return
    recipes = {r["id"]: r["title"] for r in DatabaseManager.list_recipes(user_id)}
    filtered = []
    for h in history:
        title = recipes.get(h["recipe_id"], "Unknown")
        stars = DatabaseManager.get_cooked_count(user_id, h["recipe_id"]) // 5
        filtered.append({"name": title, "date": h["cooked_date"], "stars": min(stars, 5)})

    end_week = datetime.now()
    start_week = end_week - timedelta(days=7)
    week_history = [e for e in filtered if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]
    if week_history:
        count = len(week_history)
        most_dish = Counter(e["name"] for e in week_history).most_common(1)[0][0]
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

def auth_gate_tabs():
    tabs = st.tabs([get_text("login"), get_text("register"), get_text("reset_password")])
    with tabs[0]:
        username = st.text_input(get_text("username"), key="login_username")
        password = st.text_input(get_text("password"), type="password", key="login_password")
        if st.button(get_text("login_button")):
            try:
                user_id = DatabaseManager.verify_login(username, password)
                if user_id:
                    st.session_state.update(user_id=user_id, username=username)
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            except Exception as e:
                logger.error(f"Error during login: {e}")
                st.error(get_text("db_error").format(error=e))
    with tabs[1]:
        username = st.text_input(get_text("username"), key="register_username")
        password = st.text_input(get_text("password"), type="password", key="register_password")
        sec_question = st.text_input(get_text("sec_question"), key="sec_question")
        sec_answer = st.text_input(get_text("sec_answer"), type="password", key="sec_answer")
        if st.button(get_text("create_account")):
            try:
                success, message = DatabaseManager.create_user(username, password, sec_question, sec_answer)
                if success:
                    st.success(message)
                    user_id = DatabaseManager.verify_login(username, password)
                    if user_id:
                        st.session_state.update(user_id=user_id, username=username)
                        st.rerun()
                else:
                    st.error(message)
            except Exception as e:
                logger.error(f"Error during registration: {e}")
                st.error(get_text("db_error").format(error=e))
    with tabs[2]:
        username = st.text_input(get_text("username"), key="reset_username")
        sec_answer = st.text_input(get_text("sec_answer"), type="password", key="reset_sec_answer")
        new_password = st.text_input(get_text("new_password"), type="password", key="new_password")
        if st.button(get_text("reset_button")):
            try:
                if DatabaseManager.reset_password(username, sec_answer, new_password):
                    st.success("Password reset successful.")
                else:
                    st.error("Invalid username or security answer.")
            except Exception as e:
                logger.error(f"Error during password reset: {e}")
                st.error(get_text("db_error").format(error=e))