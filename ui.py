### Sử dụng hashlib.sha256 DatabaseManager 

# import streamlit as st
# import html
# from datetime import datetime, timedelta
# from typing import Optional, Dict, List, Tuple, Any
# import logging
# from collections import defaultdict, Counter
# import hashlib  # Để hash password đơn giản

# # Thiết lập logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# if not logger.handlers:
#     logger.addHandler(handler)

# # Giả định config nếu thiếu
# APP_TITLE_EN = "RuaDen Recipe App"
# APP_TITLE_VI = "Ứng dụng Công thức RuaDen"

# # Giả định utils nếu thiếu
# VALID_UNITS = ["g", "kg", "ml", "l", "tsp", "tbsp", "cup", "piece", "pcs", "lạng", "chén", "bát"]
# def validate_unit(unit: str) -> bool:
#     return unit in VALID_UNITS

# # Văn bản đa ngôn ngữ (i18n)
# TEXT = {
#     "English": {
#         "app_title": APP_TITLE_EN,
#         "login": "🔐 Login",
#         "username": "Username",
#         "password": "Password",
#         "login_button": "Login",
#         "register": "🆕 Register",
#         "sec_question": "Security Question (for password reset)",
#         "sec_answer": "Security Answer",
#         "create_account": "Create Account",
#         "reset_password": "♻️ Reset Password",
#         "new_password": "New Password",
#         "reset_button": "Reset Password",
#         "logout": "Logout",
#         "language": "Language",
#         "title": "Title",
#         "category": "Category",
#         "instructions": "Instructions",
#         "servings": "Servings",
#         "name": "Name",
#         "quantity": "Quantity",
#         "unit": "Unit",
#         "need": "Need",
#         "have": "Have",
#         "missing": "Missing",
#         "inventory": "📦 Inventory",
#         "your_stock": "Your Stock",
#         "no_ingredients": "No ingredients yet.",
#         "unit_tips": "Unit tips: use g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
#         "add_ingredient": "Add New Ingredient",
#         "recipes": "📖 Recipes",
#         "your_recipes": "Your Recipes",
#         "no_recipes": "No recipes yet.",
#         "save_recipe": "Save Recipe",
#         "update_recipe": "Update Recipe",
#         "delete_recipe": "Delete Recipe",
#         "feasibility": "✅ Feasibility & Shopping",
#         "create_recipes_first": "Create recipes first.",
#         "you_can_cook": "Recipe Feasibility and Shopping List",
#         "none_yet": "None yet.",
#         "all_available": "All ingredients available.",
#         "cook": "Cook",
#         "missing_something": "Missing Ingredients",
#         "all_feasible": "All recipes are feasible 🎉",
#         "add_to_shopping": "Add missing to Shopping List",
#         "shopping_list": "🛒 Shopping List",
#         "empty_list": "Your shopping list is empty.",
#         "update_inventory": "Update Inventory from Shopping List",
#         "purchased": "Inventory updated with purchased items.",
#         "select_recipes_label": "Select recipes to proceed",
#         "select_purchased": "Select purchased items",
#         "sent_to_shopping": "Missing ingredients added to the shopping list.",
#         "cook_success": "Cooked successfully.",
#         "cook_failed": "Cooking failed.",
#         "adjust_recipe": "⚖️ Adjust Recipe",
#         "select_recipe": "Select Recipe",
#         "adjustment_type": "Adjustment Type",
#         "by_servings": "By Servings",
#         "by_main_ingredient": "By Main Ingredient",
#         "new_servings": "New Servings",
#         "main_ingredient": "Main Ingredient",
#         "new_quantity": "New Quantity",
#         "spice_level": "Spice Adjustment",
#         "mild": "Mild (60%)",
#         "normal": "Normal (80%)",
#         "rich": "Rich (100%)",
#         "adjusted_recipe": "Adjusted Recipe",
#         "cook_adjusted": "Cook Adjusted Recipe",
#         "add_to_shopping_adjusted": "Add Missing to Shopping List",
#         "adjusted_recipe_title": "Adjusted: {title}",
#         "no_recipe_selected": "Please select a recipe to adjust.",
#         "invalid_adjustment": "Invalid adjustment parameters.",
#         "cook_adjusted_success": "Adjusted recipe '{title}' cooked successfully.",
#         "cook_adjusted_failed": "Failed to cook adjusted recipe '{title}'.",
#         "not_logged_in": "You must be logged in to access this page.",
#         "error_title_required": "Recipe title is required.",
#         "error_ingredients_required": "At least one valid ingredient (with name and positive quantity) is required.",
#         "duplicate_recipe": "A recipe with this title already exists.",
#         "invalid_name": "Name must contain only letters, numbers, spaces, hyphens, underscores, or single quotes.",
#         "food_timeline": "🍲 Food Timeline",
#         "no_entries": "No entries found for the selected filters.",
#         "stats_week": "This week, you cooked {count} dishes. Most frequent: {dish}.",
#         "db_error": "Database error: {error}.",
#         "remove_selected": "Remove Selected Ingredients",
#     },
#     "Vietnamese": {
#         "app_title": APP_TITLE_VI,
#         "login": "🔐 Đăng nhập",
#         "username": "Tên người dùng",
#         "password": "Mật khẩu",
#         "login_button": "Đăng nhập",
#         "register": "🆕 Đăng ký",
#         "sec_question": "Câu hỏi bảo mật (để đặt lại mật khẩu)",
#         "sec_answer": "Câu trả lời bảo mật",
#         "create_account": "Tạo tài khoản",
#         "reset_password": "♻️ Đặt lại mật khẩu",
#         "new_password": "Mật khẩu mới",
#         "reset_button": "Đặt lại mật khẩu",
#         "logout": "Đăng xuất",
#         "language": "Ngôn ngữ",
#         "title": "Tiêu đề",
#         "category": "Danh mục",
#         "instructions": "Hướng dẫn",
#         "servings": "Khẩu phần",
#         "name": "Tên",
#         "quantity": "Số lượng",
#         "unit": "Đơn vị",
#         "need": "Cần",
#         "have": "Có",
#         "missing": "Thiếu",
#         "inventory": "📦 Kho hàng",
#         "your_stock": "Kho của bạn",
#         "no_ingredients": "Chưa có nguyên liệu.",
#         "unit_tips": "Mẹo đơn vị: sử dụng g, kg, ml, l, tsp, tbsp, cup, piece, cái, pcs, lạng, chén, bát.",
#         "add_ingredient": "Thêm nguyên liệu mới",
#         "recipes": "📖 Công thức",
#         "your_recipes": "Công thức của bạn",
#         "no_recipes": "Chưa có công thức nào.",
#         "save_recipe": "Lưu công thức",
#         "update_recipe": "Cập nhật công thức",
#         "delete_recipe": "Xóa công thức",
#         "feasibility": "✅ Tính khả thi & Mua sắm",
#         "create_recipes_first": "Hãy tạo công thức trước.",
#         "you_can_cook": "Tính khả thi công thức và Danh sách mua sắm",
#         "none_yet": "Chưa có.",
#         "all_available": "Tất cả nguyên liệu có sẵn.",
#         "cook": "Nấu",
#         "missing_something": "Thiếu nguyên liệu",
#         "all_feasible": "Tất cả công thức đều khả thi 🎉",
#         "add_to_shopping": "Thêm thiếu vào Danh sách mua sắm",
#         "shopping_list": "🛒 Danh sách mua sắm",
#         "empty_list": "Danh sách mua sắm của bạn trống.",
#         "update_inventory": "Cập nhật kho từ Danh sách mua sắm",
#         "purchased": "Kho đã được cập nhật với các mặt hàng đã mua.",
#         "select_recipes_label": "Chọn công thức để tiếp tục",
#         "select_purchased": "Chọn các mặt hàng đã mua",
#         "sent_to_shopping": "Nguyên liệu thiếu đã được thêm vào danh sách mua sắm.",
#         "cook_success": "Nấu thành công.",
#         "cook_failed": "Nấu thất bại.",
#         "adjust_recipe": "⚖️ Điều chỉnh Công thức",
#         "select_recipe": "Chọn Công thức",
#         "adjustment_type": "Loại điều chỉnh",
#         "by_servings": "Theo Khẩu phần",
#         "by_main_ingredient": "Theo Nguyên liệu chính",
#         "new_servings": "Khẩu phần mới",
#         "main_ingredient": "Nguyên liệu chính",
#         "new_quantity": "Số lượng mới",
#         "spice_level": "Điều chỉnh Gia vị",
#         "mild": "Nhẹ (60%)",
#         "normal": "Bình thường (80%)",
#         "rich": "Đậm (100%)",
#         "adjusted_recipe": "Công thức đã điều chỉnh",
#         "cook_adjusted": "Nấu Công thức đã điều chỉnh",
#         "add_to_shopping_adjusted": "Thêm thiếu vào Danh sách mua sắm",
#         "adjusted_recipe_title": "Đã điều chỉnh: {title}",
#         "no_recipe_selected": "Vui lòng chọn một công thức để điều chỉnh.",
#         "invalid_adjustment": "Tham số điều chỉnh không hợp lệ.",
#         "cook_adjusted_success": "Công thức đã điều chỉnh '{title}' nấu thành công.",
#         "cook_adjusted_failed": "Không thể nấu công thức đã điều chỉnh '{title}'.",
#         "not_logged_in": "Bạn phải đăng nhập để truy cập trang này.",
#         "error_title_required": "Tiêu đề công thức là bắt buộc.",
#         "error_ingredients_required": "Cần ít nhất một nguyên liệu hợp lệ (có tên và số lượng dương).",
#         "duplicate_recipe": "Công thức với tiêu đề này đã tồn tại.",
#         "invalid_name": "Tên chỉ được chứa chữ cái, số, khoảng trắng, dấu gạch ngang, gạch dưới hoặc dấu nháy đơn.",
#         "food_timeline": "🍲 Dòng thời gian món đã nấu",
#         "no_entries": "Không tìm thấy mục nào cho bộ lọc đã chọn.",
#         "stats_week": "Tuần này, bạn đã nấu {count} món. Món thường xuyên nhất: {dish}.",
#         "db_error": "Lỗi cơ sở dữ liệu: {error}.",
#         "remove_selected": "Xóa các nguyên liệu đã chọn",
#     }
# }

# # Danh sách các tên được export
# __all__ = [
#     'topbar_account', 'inject_css', 'get_text', 'current_user_id', 'initialize_session_state',
#     'inventory_page', 'recipes_page', 'feasibility_page', 'shopping_list_page',
#     'recipe_adjustment_page', 'food_timeline_page', 'auth_gate_tabs', 'main'
# ]

# def topbar_account() -> None:
#     """Hiển thị topbar với thông tin tài khoản và tùy chọn ngôn ngữ."""
#     try:
#         user_id = current_user_id()
#         username = st.session_state.get("username", "Unknown")
#         if not user_id:
#             st.markdown('<div id="topbar-account">Not logged in</div>', unsafe_allow_html=True)
#             return
#         col1, col2, col3 = st.columns([2, 1, 1])
#         with col1:
#             st.markdown(f'<div id="topbar-account">{get_text("username")}: {html.escape(username)}</div>', unsafe_allow_html=True)
#         with col2:
#             lang_options = ["English", "Vietnamese"]
#             current_lang_index = 0 if st.session_state.get("language") == "English" else 1
#             lang = st.selectbox(get_text("language"), lang_options, index=current_lang_index, key="language_selector")
#             if lang != st.session_state.get("language", "English"):
#                 st.session_state.language = lang
#                 logger.info(f"User {username} changed language to {lang}")
#                 st.rerun()
#         with col3:
#             if st.button(get_text("logout")):
#                 st.session_state.clear()
#                 logger.info(f"User {username} logged out")
#                 st.rerun()
#     except Exception as e:
#         logger.error(f"Error in topbar_account: {e}")
#         st.error("Error displaying account topbar. Please refresh the page.")

# def inject_css() -> None:
#     """Tiêm CSS tùy chỉnh để định dạng ứng dụng Streamlit."""
#     try:
#         st.markdown(
#             """
#             <style>
#                 .block-container {
#                     padding-top: 5rem;
#                     padding-bottom: 2rem;
#                     max-width: 980px;
#                 }
#                 .stTextInput > div > div > input,
#                 .stNumberInput > div > div > input,
#                 textarea {
#                     border-radius: 12px !important;
#                     border: 1px solid #e6e6e6 !important;
#                     padding: .55rem .8rem !important;
#                 }
#                 .stButton > button {
#                     background: #111 !important;
#                     color: #fff !important;
#                     border: none !important;
#                     border-radius: 14px !important;
#                     padding: .55rem 1rem !important;
#                     font-weight: 500 !important;
#                     transition: transform .12s ease, opacity .12s ease;
#                 }
#                 .stButton > button:hover {
#                     transform: translateY(-1px);
#                     opacity: .95;
#                 }
#                 table {
#                     border-collapse: collapse;
#                     width: 100%;
#                 }
#                 th, td {
#                     padding: 8px 10px;
#                     border-bottom: 1px solid #eee;
#                 }
#                 th {
#                     color: #666;
#                     font-weight: 600;
#                 }
#                 td {
#                     color: #222;
#                 }
#                 .stTabs [data-baseweb="tab-list"] {
#                     gap: .25rem;
#                     margin-top: 1rem;
#                 }
#                 .stTabs [data-baseweb="tab"] {
#                     padding: .6rem 1rem;
#                 }
#                 .streamlit-expanderHeader {
#                     font-weight: 600;
#                 }
#                 #topbar-account {
#                     margin-bottom: 1rem;
#                 }
#                 .food-card {
#                     border: 1px solid #eee;
#                     border-radius: 12px;
#                     padding: 1rem;
#                     margin-bottom: 1rem;
#                     background-color: #f9f9f9;
#                 }
#                 .dish-name {
#                     font-weight: bold;
#                     font-size: 1.2em;
#                 }
#                 .stars {
#                     font-size: 1.2em;
#                     color: #FFD700;
#                     text-align: right;
#                 }
#                 @media (max-width: 600px) {
#                     .block-container {
#                         padding-top: 4rem;
#                         padding-left: 1rem;
#                         padding-right: 1rem;
#                     }
#                     .stButton > button {
#                         width: 100%;
#                         margin-bottom: 0.5rem;
#                     }
#                     .stTabs [data-baseweb="tab-list"] {
#                         margin-top: 0.5rem;
#                     }
#                 }
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )
#     except Exception as e:
#         logger.error(f"Lỗi tiêm CSS: {e}")
#         st.error("Không thể áp dụng kiểu dáng tùy chỉnh. Tiếp tục với kiểu mặc định.")

# def get_text(key: str) -> str:
#     """Lấy văn bản đa ngôn ngữ dựa trên ngôn ngữ người dùng."""
#     lang = st.session_state.get("language", "English")
#     return TEXT.get(lang, TEXT["English"]).get(key, key)

# def current_user_id() -> Optional[int]:
#     """Lấy user_id hiện tại từ session_state."""
#     return st.session_state.get("user_id")

# def initialize_session_state() -> None:
#     """Khởi tạo các biến trạng thái phiên nếu chưa có."""
#     defaults = {
#         "user_id": None,
#         "username": None,
#         "language": "English",
#         "editing_recipe_id": None,
#         "recipe_form_data": {
#             "title": "",
#             "category": "",
#             "instructions": "",
#             "is_signature": False,
#             "servings": 1.0,
#             "ingredients": [
#                 {"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}
#             ],
#         },
#         "shopping_list_data": [],
#         "adjusted_recipe": None,
#         "inventory_key": None,
#     }
#     for key, value in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = value

# # STUB cho business_logic
# def recipe_feasibility(recipe: Dict, user_id: int) -> Tuple[bool, List[Dict]]:
#     """Stub: Kiểm tra feasibility đơn giản."""
#     inventory = DatabaseManager.list_inventory(user_id)
#     inv_dict = {item["name"]: item["quantity"] for item in inventory}
#     shorts = []
#     feasible = True
#     for ing in recipe["ingredients"]:
#         if ing["name"] and ing["quantity"] > 0:
#             have = inv_dict.get(ing["name"], 0)
#             if have < ing["quantity"]:
#                 feasible = False
#                 shorts.append({
#                     "name": ing["name"],
#                     "needed_qty": ing["quantity"],
#                     "needed_unit": ing["unit"],
#                     "have_qty": have,
#                     "have_unit": ing["unit"],
#                     "missing_qty_disp": ing["quantity"] - have,
#                     "missing_unit_disp": ing["unit"]
#                 })
#     return feasible, shorts

# def consume_ingredients_for_recipe(recipe: Dict, user_id: int) -> bool:
#     """Stub: Consume ingredients."""
#     return True

# # CLASS DatabaseManager STUB (in-memory) - giữ nguyên từ trước
# class DatabaseManager:
#     _users: Dict[str, Dict] = {}
#     _next_user_id = 1
#     _inventory: Dict[int, List[Dict]] = {}
#     _recipes: Dict[int, List[Dict]] = {}
#     _cooked_history: Dict[int, List[Dict]] = {}
#     _cooked_count: Dict[tuple, int] = {}

#     @classmethod
#     def verify_login(cls, username: str, password: str) -> Tuple[bool, Any]:
#         if not username or not password or len(password) < 8:
#             return False, "Invalid credentials or password too short."
#         user = cls._users.get(username)
#         if user and user["password_hash"] == hashlib.sha256(password.encode()).hexdigest():
#             return True, user["id"]
#         return False, "Invalid username or password."

#     @classmethod
#     def create_user(cls, username: str, password: str, sec_question: str, sec_answer: str) -> Tuple[bool, str]:
#         if not all([username.strip(), password.strip(), sec_question.strip(), sec_answer.strip()]):
#             return False, "All fields required."
#         if len(password) < 8:
#             return False, "Password must be at least 8 characters."
#         if username in cls._users:
#             return False, "Username already exists."
#         password_hash = hashlib.sha256(password.encode()).hexdigest()
#         sec_hash = hashlib.sha256(sec_answer.encode()).hexdigest()
#         user_id = cls._next_user_id
#         cls._users[username] = {
#             "id": user_id,
#             "password_hash": password_hash,
#             "sec_question": sec_question,
#             "sec_answer_hash": sec_hash
#         }
#         cls._next_user_id += 1
#         cls._inventory[user_id] = []
#         cls._recipes[user_id] = []
#         cls._cooked_history[user_id] = []
#         return True, "User created successfully."

#     @classmethod
#     def reset_password(cls, username: str, sec_answer: str, new_password: str) -> Tuple[bool, str]:
#         if not all([username.strip(), sec_answer.strip(), new_password.strip()]):
#             return False, "All fields required."
#         if len(new_password) < 8:
#             return False, "New password must be at least 8 characters."
#         user = cls._users.get(username)
#         if not user:
#             return False, "User not found."
#         if user["sec_answer_hash"] == hashlib.sha256(sec_answer.encode()).hexdigest():
#             user["password_hash"] = hashlib.sha256(new_password.encode()).hexdigest()
#             return True, "Password reset successfully."
#         return False, "Invalid security answer."

#     @classmethod
#     def list_inventory(cls, user_id: int) -> List[Dict]:
#         return cls._inventory.get(user_id, [])

#     @classmethod
#     def add_inventory_item(cls, user_id: int, name: str, quantity: float, unit: str) -> Tuple[bool, str]:
#         if not validate_unit(unit):
#             return False, "Invalid unit."
#         item = {"name": name, "quantity": quantity, "unit": unit}
#         inv = cls._inventory.setdefault(user_id, [])
#         for i in inv:
#             if i["name"].lower() == name.lower():  # Case-insensitive match
#                 i["quantity"] += quantity
#                 return True, "Inventory updated."
#         inv.append(item)
#         return True, "Item added to inventory."

#     @classmethod
#     def list_recipes(cls, user_id: int) -> List[Dict]:
#         return cls._recipes.get(user_id, [])

#     @classmethod
#     def get_recipe_by_title(cls, user_id: int, title: str) -> Optional[Dict]:
#         recipes = cls._recipes.get(user_id, [])
#         for r in recipes:
#             if r["title"] == title:
#                 return r
#         return None

#     @classmethod
#     def create_recipe(cls, user_id: int, recipe_data: Dict) -> Tuple[bool, str]:
#         if not recipe_data["title"].strip():
#             return False, "Title required."
#         if not any(ing["name"].strip() and ing["quantity"] > 0 for ing in recipe_data["ingredients"]):
#             return False, "Valid ingredients required."
#         recipe = recipe_data.copy()
#         recipe["id"] = len(cls._recipes.get(user_id, [])) + 1
#         recipes = cls._recipes.setdefault(user_id, [])
#         if any(r["title"] == recipe["title"] for r in recipes):
#             return False, "Duplicate title."
#         recipes.append(recipe)
#         return True, "Recipe saved."

#     @classmethod
#     def delete_recipe(cls, user_id: int, recipe_id: int) -> Tuple[bool, str]:
#         recipes = cls._recipes.get(user_id, [])
#         for i, r in enumerate(recipes):
#             if r["id"] == recipe_id:
#                 del recipes[i]
#                 return True, "Recipe deleted."
#         return False, "Recipe not found."

#     @classmethod
#     def log_cooked_recipe(cls, user_id: int, recipe_id: int) -> None:
#         history = cls._cooked_history.setdefault(user_id, [])
#         history.append({"recipe_id": recipe_id, "cooked_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
#         key = (user_id, recipe_id)
#         cls._cooked_count[key] = cls._cooked_count.get(key, 0) + 1

#     @classmethod
#     def list_cooked_history(cls, user_id: int) -> List[Dict]:
#         return cls._cooked_history.get(user_id, [])

#     @classmethod
#     def get_cooked_count(cls, user_id: int, recipe_id: int) -> int:
#         return cls._cooked_count.get((user_id, recipe_id), 0)

# # Thêm user mẫu
# DatabaseManager._users["admin1234"] = {
#     "id": 1,
#     "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
#     "sec_question": "What is your pet's name?",
#     "sec_answer_hash": hashlib.sha256("dog".encode()).hexdigest()
# }
# DatabaseManager._inventory[1] = []
# DatabaseManager._recipes[1] = []
# DatabaseManager._cooked_history[1] = []
# DatabaseManager._next_user_id = 2

# def inventory_page() -> None:
#     """Hiển thị và quản lý trang kho hàng."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     st.header(get_text("your_stock"))
#     inventory = DatabaseManager.list_inventory(user_id)
#     if not inventory:
#         st.info(get_text("no_ingredients"))
#     else:
#         cols = st.columns([2, 1, 1])
#         cols[0].subheader(get_text("name"))
#         cols[1].subheader(get_text("quantity"))
#         cols[2].subheader(get_text("unit"))
#         for item in inventory:
#             cols = st.columns([2, 1, 1])
#             cols[0].write(item["name"])
#             cols[1].write(f"{item['quantity']:.2f}")
#             cols[2].write(item["unit"])
#     st.subheader(get_text("add_ingredient"))
#     st.caption(get_text("unit_tips"))
#     with st.form(key="add_inventory_form"):
#         name = st.text_input(get_text("name"), max_chars=50)
#         quantity = st.number_input(get_text("quantity"), min_value=0.0, step=0.1)
#         unit = st.selectbox(get_text("unit"), options=VALID_UNITS)
#         submit = st.form_submit_button(get_text("add_ingredient"))
#         if submit:
#             if not name.strip() or quantity <= 0:
#                 st.error(get_text("error_ingredients_required"))
#             elif not validate_unit(unit):
#                 st.error("Invalid unit.")
#             else:
#                 success, message = DatabaseManager.add_inventory_item(user_id, name.strip(), quantity, unit)
#                 if success:
#                     st.success(message)
#                     st.rerun()
#                 else:
#                     st.error(message)

# def recipes_page() -> None:
#     """Hiển thị và quản lý trang công thức - FIXED: Buttons ngoài form, checkbox cho remove."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     st.header(get_text("your_recipes"))
#     recipes = DatabaseManager.list_recipes(user_id)
#     if not recipes:
#         st.info(get_text("no_recipes"))
#     for recipe in recipes:
#         with st.expander(f"{recipe['title']} ({recipe.get('servings', 1)} {get_text('servings')})"):
#             st.write(f"{get_text('category')}: {recipe.get('category', 'N/A')}")
#             st.write(f"{get_text('instructions')}: {recipe.get('instructions', 'N/A')}")
#             st.write(f"{get_text('servings')}: {recipe.get('servings', 1)}")
#             st.write(f"Signature: {'Yes' if recipe.get('is_signature', False) else 'No'}")
#             st.subheader(get_text("ingredients"))
#             cols = st.columns([2, 1, 1, 1])
#             cols[0].write(get_text("name"))
#             cols[1].write(get_text("quantity"))
#             cols[2].write(get_text("unit"))
#             cols[3].write("Spice")
#             for ing in recipe["ingredients"]:
#                 cols = st.columns([2, 1, 1, 1])
#                 cols[0].write(ing["name"])
#                 cols[1].write(ing["quantity"])
#                 cols[2].write(ing["unit"])
#                 cols[3].write("Yes" if ing["is_spice"] else "No")
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button(get_text("update_recipe"), key=f"edit_{recipe['id']}"):
#                     st.session_state.editing_recipe_id = recipe["id"]
#                     st.session_state.recipe_form_data = recipe.copy()  # Copy để tránh mutate
#                     st.rerun()
#             with col2:
#                 if st.button(get_text("delete_recipe"), key=f"delete_{recipe['id']}"):
#                     success, message = DatabaseManager.delete_recipe(user_id, recipe["id"])
#                     if success:
#                         st.success(message)
#                         st.rerun()
#                     else:
#                         st.error(message)
#     st.subheader(get_text("save_recipe"))
#     recipe_data = st.session_state.recipe_form_data
#     # Button Add ngoài form
#     if st.button(get_text("add_ingredient")):
#         recipe_data["ingredients"].append({"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False})
#         st.rerun()
#     # Form cho inputs
#     with st.form(key="recipe_form"):
#         recipe_data["title"] = st.text_input(get_text("title"), value=recipe_data["title"], max_chars=100)
#         recipe_data["category"] = st.text_input(get_text("category"), value=recipe_data["category"], max_chars=50)
#         recipe_data["instructions"] = st.text_area(get_text("instructions"), value=recipe_data["instructions"])
#         recipe_data["servings"] = st.number_input(get_text("servings"), min_value=1.0, step=0.5, value=recipe_data.get("servings", 1.0))
#         recipe_data["is_signature"] = st.checkbox("Signature Dish", value=recipe_data.get("is_signature", False))
#         st.subheader(get_text("ingredients"))
#         # Thêm checkbox remove trong form (batch)
#         for i, ing in enumerate(recipe_data["ingredients"]):
#             cols = st.columns([2, 1, 1, 1, 1])  # Thêm cột cho checkbox remove
#             ing["name"] = cols[0].text_input(get_text("name"), value=ing["name"], max_chars=50, key=f"ing_name_{i}")
#             ing["quantity"] = cols[1].number_input(get_text("quantity"), min_value=0.0, step=0.1, value=ing["quantity"], key=f"ing_qty_{i}")
#             unit_index = VALID_UNITS.index(ing["unit"]) if ing["unit"] in VALID_UNITS else 0
#             ing["unit"] = cols[2].selectbox(get_text("unit"), options=VALID_UNITS, index=unit_index, key=f"ing_unit_{i}")
#             ing["is_spice"] = cols[3].checkbox("Spice", value=ing["is_spice"], key=f"ing_spice_{i}")
#             # Checkbox remove (trong form, batch)
#             cols[4].checkbox("Remove?", key=f"remove_ing_{i}")
#         submit = st.form_submit_button(get_text("save_recipe") if not st.session_state.editing_recipe_id else get_text("update_recipe"))
#     # Button Remove Selected ngoài form
#     if st.button(get_text("remove_selected")):
#         to_remove = [i for i, ing in enumerate(recipe_data["ingredients"]) if st.session_state.get(f"remove_ing_{i}", False)]
#         for i in sorted(to_remove, reverse=True):
#             del recipe_data["ingredients"][i]
#         # Clear checkboxes sau remove
#         for key in list(st.session_state.keys()):
#             if key.startswith("remove_ing_"):
#                 del st.session_state[key]
#         st.rerun()
#     if submit:
#         if not recipe_data["title"].strip():
#             st.error(get_text("error_title_required"))
#         elif not any(ing["name"].strip() and ing["quantity"] > 0 for ing in recipe_data["ingredients"]):
#             st.error(get_text("error_ingredients_required"))
#         else:
#             if st.session_state.editing_recipe_id:
#                 success, message = DatabaseManager.delete_recipe(user_id, st.session_state.editing_recipe_id)
#                 if not success:
#                     st.error(message)
#                     return
#             success, message = DatabaseManager.create_recipe(user_id, recipe_data)
#             if success:
#                 st.session_state.editing_recipe_id = None
#                 st.session_state.recipe_form_data = {
#                     "title": "",
#                     "category": "",
#                     "instructions": "",
#                     "is_signature": False,
#                     "servings": 1.0,
#                     "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#                 }
#                 st.success(message)
#                 st.rerun()
#             else:
#                 st.error(message)

# def feasibility_page() -> None:
#     """Hiển thị trang tính khả thi và danh sách mua sắm."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     recipes = DatabaseManager.list_recipes(user_id)
#     if not recipes:
#         st.info(get_text("create_recipes_first"))
#         return
#     st.header(get_text("you_can_cook"))
#     selected_recipes = st.multiselect(get_text("select_recipes_label"), [r["title"] for r in recipes], key="feasibility_select")
#     if not selected_recipes:
#         st.info(get_text("none_yet"))
#         return
#     all_feasible = True
#     for title in selected_recipes:
#         recipe = DatabaseManager.get_recipe_by_title(user_id, title)
#         if not recipe:
#             continue
#         feasible, shorts = recipe_feasibility(recipe, user_id)
#         with st.expander(f"{recipe['title']} {'✅' if feasible else '❌'}"):
#             if feasible:
#                 st.success(get_text("all_available"))
#                 if st.button(get_text("cook"), key=f"cook_{recipe.get('id', 0)}"):
#                     if consume_ingredients_for_recipe(recipe, user_id):
#                         DatabaseManager.log_cooked_recipe(user_id, recipe.get("id", 1))
#                         st.success(get_text("cook_success"))
#                         st.rerun()
#                     else:
#                         st.error(get_text("cook_failed"))
#             else:
#                 all_feasible = False
#                 st.warning(get_text("missing_something"))
#                 cols = st.columns([2, 1, 1, 1])
#                 cols[0].write(get_text("name"))
#                 cols[1].write(get_text("need"))
#                 cols[2].write(get_text("have"))
#                 cols[3].write(get_text("missing"))
#                 for short in shorts:
#                     cols = st.columns([2, 1, 1, 1])
#                     cols[0].write(short["name"])
#                     cols[1].write(f"{short['needed_qty']:.2f} {short['needed_unit']}")
#                     cols[2].write(f"{short['have_qty']:.2f} {short['have_unit']}")
#                     cols[3].write(f"{short['missing_qty_disp']:.2f} {short['missing_unit_disp']}")
#                 if st.button(get_text("add_to_shopping"), key=f"shop_{recipe.get('id', 0)}"):
#                     st.session_state.shopping_list_data.extend([
#                         {"name": s["name"], "quantity": s["missing_qty_disp"], "unit": s["missing_unit_disp"]}
#                         for s in shorts
#                     ])
#                     st.success(get_text("sent_to_shopping"))
#                     st.rerun()
#     if all_feasible and selected_recipes:
#         st.success(get_text("all_feasible"))

# def shopping_list_page() -> None:
#     """Hiển thị và quản lý danh sách mua sắm."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     st.header(get_text("shopping_list"))
#     shopping_list = st.session_state.shopping_list_data
#     if not shopping_list:
#         st.info(get_text("empty_list"))
#         return
#     selected_items = []
#     cols = st.columns([1, 2, 1, 1])
#     cols[0].write("")
#     cols[1].write(get_text("name"))
#     cols[2].write(get_text("quantity"))
#     cols[3].write(get_text("unit"))
#     for i, item in enumerate(shopping_list):
#         cols = st.columns([1, 2, 1, 1])
#         selected = cols[0].checkbox("", key=f"shop_item_{i}")
#         cols[1].write(item["name"])
#         cols[2].write(f"{item['quantity']:.2f}")
#         cols[3].write(item["unit"])
#         if selected:
#             selected_items.append(i)
#     if st.button(get_text("update_inventory")):
#         for i in sorted(selected_items, reverse=True):
#             item = shopping_list[i]
#             success, message = DatabaseManager.add_inventory_item(user_id, item["name"], float(item["quantity"]), item["unit"])
#             if success:
#                 del shopping_list[i]
#         st.session_state.shopping_list_data = shopping_list
#         st.success(get_text("purchased"))
#         st.rerun()

# def recipe_adjustment_page() -> None:
#     """Hiển thị trang điều chỉnh công thức."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     st.header(get_text("adjust_recipe"))
#     recipes = DatabaseManager.list_recipes(user_id)
#     recipe_titles = [r["title"] for r in recipes]
#     selected_recipe = st.selectbox(get_text("select_recipe"), [""] + recipe_titles)
#     if not selected_recipe:
#         st.info(get_text("no_recipe_selected"))
#         return
#     recipe = DatabaseManager.get_recipe_by_title(user_id, selected_recipe)
#     if not recipe:
#         st.error(get_text("no_recipe_selected"))
#         return
#     adjustment_type = st.selectbox(get_text("adjustment_type"), [get_text("by_servings"), get_text("by_main_ingredient")])
#     new_recipe = recipe.copy()
#     new_recipe["ingredients"] = [{"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": ing["is_spice"]} for ing in recipe["ingredients"]]
#     factor = 1.0
#     if adjustment_type == get_text("by_servings"):
#         new_servings = st.number_input(get_text("new_servings"), min_value=0.1, step=0.1, value=recipe.get("servings", 1.0))
#         if new_servings > 0:
#             factor = new_servings / recipe.get("servings", 1.0)
#             new_recipe["servings"] = new_servings
#     else:
#         main_ingredients = [ing["name"] for ing in recipe["ingredients"] if ing["name"]]
#         if not main_ingredients:
#             st.error("No ingredients to adjust.")
#             return
#         main_ingredient = st.selectbox(get_text("main_ingredient"), main_ingredients)
#         new_quantity = st.number_input(get_text("new_quantity"), min_value=0.0, step=0.1, value=next((ing["quantity"] for ing in recipe["ingredients"] if ing["name"] == main_ingredient), 0.0))
#         orig_qty = next((ing["quantity"] for ing in recipe["ingredients"] if ing["name"] == main_ingredient), 0)
#         if orig_qty > 0:
#             factor = new_quantity / orig_qty
#     spice_level = st.selectbox(get_text("spice_level"), [get_text("mild"), get_text("normal"), get_text("rich")])
#     spice_map = {
#         get_text("mild"): 0.6,
#         get_text("normal"): 0.8,
#         get_text("rich"): 1.0
#     }
#     spice_factor = spice_map.get(spice_level, 1.0)
#     for ing in new_recipe["ingredients"]:
#         ing["quantity"] *= factor
#         if ing["is_spice"]:
#             ing["quantity"] *= spice_factor
#     new_recipe["title"] = get_text("adjusted_recipe_title").format(title=recipe["title"])
#     st.session_state.adjusted_recipe = new_recipe
#     st.subheader(get_text("adjusted_recipe"))
#     cols = st.columns([2, 1, 1, 1])
#     cols[0].write(get_text("name"))
#     cols[1].write(get_text("quantity"))
#     cols[2].write(get_text("unit"))
#     cols[3].write("Spice")
#     for ing in new_recipe["ingredients"]:
#         if ing["name"]:
#             cols = st.columns([2, 1, 1, 1])
#             cols[0].write(ing["name"])
#             cols[1].write(f"{ing['quantity']:.2f}")
#             cols[2].write(ing["unit"])
#             cols[3].write("Yes" if ing["is_spice"] else "No")
#     feasible, shorts = recipe_feasibility(new_recipe, user_id)
#     if feasible:
#         st.success(get_text("all_available"))
#         if st.button(get_text("cook_adjusted")):
#             if consume_ingredients_for_recipe(new_recipe, user_id):
#                 DatabaseManager.log_cooked_recipe(user_id, recipe.get("id", 1))
#                 st.success(get_text("cook_adjusted_success").format(title=new_recipe["title"]))
#                 st.rerun()
#             else:
#                 st.error(get_text("cook_adjusted_failed").format(title=new_recipe["title"]))
#     else:
#         st.warning(get_text("missing_something"))
#         cols = st.columns([2, 1, 1, 1])
#         cols[0].write(get_text("name"))
#         cols[1].write(get_text("need"))
#         cols[2].write(get_text("have"))
#         cols[3].write(get_text("missing"))
#         for short in shorts:
#             cols = st.columns([2, 1, 1, 1])
#             cols[0].write(short["name"])
#             cols[1].write(f"{short['needed_qty']:.2f} {short['needed_unit']}")
#             cols[2].write(f"{short['have_qty']:.2f} {short['have_unit']}")
#             cols[3].write(f"{short['missing_qty_disp']:.2f} {short['missing_unit_disp']}")
#         if st.button(get_text("add_to_shopping_adjusted")):
#             st.session_state.shopping_list_data.extend([
#                 {"name": s["name"], "quantity": s["missing_qty_disp"], "unit": s["missing_unit_disp"]}
#                 for s in shorts
#             ])
#             st.success(get_text("sent_to_shopping"))
#             st.rerun()

# def food_timeline_page() -> None:
#     """Hiển thị dòng thời gian các món đã nấu."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     st.header(get_text("food_timeline"))
#     history = DatabaseManager.list_cooked_history(user_id)
#     recipes = {r["id"]: r["title"] for r in DatabaseManager.list_recipes(user_id)}
#     enriched = []
#     for entry in history:
#         recipe_title = recipes.get(entry["recipe_id"], "Unknown")
#         count = DatabaseManager.get_cooked_count(user_id, entry["recipe_id"])
#         enriched.append({"name": recipe_title, "date": entry["cooked_date"], "stars": min(count, 5)})
#     tag_filter = st.text_input("Search by dish name", "")
#     week_filter = st.checkbox("This week")
#     day_filter = st.date_input("Filter by day", value=None, min_value=datetime.now() - timedelta(days=365))
#     filtered = [e for e in enriched if (not tag_filter or tag_filter.lower() in e["name"].lower())]
#     if week_filter:
#         current_date = datetime.now()
#         start_week = current_date - timedelta(days=current_date.weekday())
#         end_week = start_week + timedelta(days=6)
#         filtered = [e for e in filtered if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]
#     if day_filter:
#         try:
#             filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date() == day_filter.date()]
#         except:
#             pass
#     if not filtered:
#         st.info(get_text("no_entries"))
#         return
#     filtered.sort(key=lambda e: e["date"], reverse=True)
#     current_date = datetime.now()
#     start_week = current_date - timedelta(days=current_date.weekday())
#     end_week = start_week + timedelta(days=6)
#     week_history = [e for e in enriched if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]
#     if week_history:
#         count = len(week_history)
#         most_dish = Counter(e["name"] for e in week_history).most_common(1)[0][0] if week_history else "None"
#         st.info(get_text("stats_week").format(count=count, dish=most_dish))
#     groups = defaultdict(list)
#     for e in filtered:
#         groups[datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date()].append(e)
#     for day in sorted(groups.keys(), reverse=True):
#         with st.container():
#             st.markdown('<div class="food-card">', unsafe_allow_html=True)
#             st.subheader(day.strftime("%Y-%m-%d"))
#             for e in groups[day]:
#                 col1, col2 = st.columns([5, 1])
#                 with col1:
#                     st.markdown(f"<span class='dish-name'>{html.escape(e['name'])}</span>", unsafe_allow_html=True)
#                 with col2:
#                     st.markdown(f"<span class='stars'>{'⭐' * e['stars']}</span>", unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

# def auth_gate_tabs() -> None:
#     """Hiển thị các tab xác thực."""
#     tabs = st.tabs([get_text("login"), get_text("register"), get_text("reset_password")])
#     with tabs[0]:
#         username = st.text_input(get_text("username"), key="login_username", max_chars=50)
#         password = st.text_input(get_text("password"), type="password", key="login_password")
#         if st.button(get_text("login_button"), key="login_btn"):
#             if not username.strip() or not password.strip():
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             if len(password) < 8:
#                 st.error("Password must be at least 8 characters.")
#                 return
#             try:
#                 success, result = DatabaseManager.verify_login(username.strip(), password)
#                 if success:
#                     st.session_state.update(user_id=result, username=username.strip())
#                     st.success(f"{get_text('login_button')} successful!")
#                     st.rerun()
#                 else:
#                     st.error(result)
#             except Exception as e:
#                 logger.error(f"Login error for {username}: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))
#     with tabs[1]:
#         username = st.text_input(get_text("username"), key="register_username", max_chars=50, help=get_text("invalid_name"))
#         password = st.text_input(get_text("password"), type="password", key="register_password", help="Minimum 8 characters, letters, numbers")
#         sec_question = st.text_input(get_text("sec_question"), key="sec_question", max_chars=200)
#         sec_answer = st.text_input(get_text("sec_answer"), type="password", key="sec_answer", max_chars=100)
#         if st.button(get_text("create_account"), key="register_btn"):
#             if not all([username.strip(), password.strip(), sec_question.strip(), sec_answer.strip()]):
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             if len(password) < 8:
#                 st.error("Password must be at least 8 characters.")
#                 return
#             try:
#                 success, message = DatabaseManager.create_user(username.strip(), password, sec_question.strip(), sec_answer.strip())
#                 if success:
#                     st.success(message)
#                     login_success, login_id = DatabaseManager.verify_login(username.strip(), password)
#                     if login_success:
#                         st.session_state.update(user_id=login_id, username=username.strip())
#                         st.rerun()
#                     else:
#                         st.error("Auto-login failed.")
#                 else:
#                     st.error(message)
#             except Exception as e:
#                 logger.error(f"Register error for {username}: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))
#     with tabs[2]:
#         username = st.text_input(get_text("username"), key="reset_username", max_chars=50)
#         sec_answer = st.text_input(get_text("sec_answer"), type="password", key="reset_sec_answer", max_chars=100)
#         new_password = st.text_input(get_text("new_password"), type="password", key="new_password")
#         if st.button(get_text("reset_button"), key="reset_btn"):
#             if not all([username.strip(), sec_answer.strip(), new_password.strip()]):
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             if len(new_password) < 8:
#                 st.error("New password must be at least 8 characters.")
#                 return
#             try:
#                 success, message = DatabaseManager.reset_password(username.strip(), sec_answer.strip(), new_password)
#                 if success:
#                     st.success(message)
#                 else:
#                     st.error(message)
#             except Exception as e:
#                 logger.error(f"Reset error for {username}: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

# def main() -> None:
#     """Điểm vào ứng dụng chính."""
#     try:
#         initialize_session_state()
#         inject_css()
#         st.title(get_text("app_title"))
#         if current_user_id():
#             topbar_account()
#             tabs = st.tabs([
#                 get_text("inventory"),
#                 get_text("recipes"),
#                 get_text("feasibility"),
#                 get_text("shopping_list"),
#                 get_text("adjust_recipe"),
#                 get_text("food_timeline")
#             ])
#             with tabs[0]:
#                 inventory_page()
#             with tabs[1]:
#                 recipes_page()
#             with tabs[2]:
#                 feasibility_page()
#             with tabs[3]:
#                 shopping_list_page()
#             with tabs[4]:
#                 recipe_adjustment_page()
#             with tabs[5]:
#                 food_timeline_page()
#         else:
#             auth_gate_tabs()
#     except Exception as e:
#         logger.error(f"Error in main: {e}")
#         st.error(get_text("db_error").format(error=str(e)))

# if __name__ == "__main__":
#     main()






### hoàn thành Sử dụng hashlib.sha256 DatabaseManager 

# import streamlit as st
# import html
# from datetime import datetime, timedelta
# from typing import Optional, Dict, List, Tuple, Any
# import logging
# from collections import defaultdict, Counter
# import hashlib
# import re

# # Thiết lập logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# if not logger.handlers:
#     logger.addHandler(handler)

# # Constants
# APP_TITLE_EN = "RuaDen Recipe App"
# APP_TITLE_VI = "Ứng dụng Công thức RuaDen"
# VALID_UNITS = ["g", "kg", "ml", "l", "tsp", "tbsp", "cup", "piece", "pcs", "lạng", "chén", "bát"]

# # Văn bản đa ngôn ngữ
# TEXT = {
#     "English": {
#         "app_title": APP_TITLE_EN,
#         "login": "🔐 Login",
#         "username": "Username",
#         "password": "Password",
#         "login_button": "Login",
#         "register": "🆕 Register",
#         "sec_question": "Security Question (for password reset)",
#         "sec_answer": "Security Answer",
#         "create_account": "Create Account",
#         "reset_password": "♻️ Reset Password",
#         "new_password": "New Password",
#         "reset_button": "Reset Password",
#         "logout": "Logout",
#         "language": "Language",
#         "title": "Title",
#         "category": "Category",
#         "instructions": "Instructions",
#         "servings": "Servings",
#         "name": "Name",
#         "quantity": "Quantity",
#         "unit": "Unit",
#         "need": "Need",
#         "have": "Have",
#         "missing": "Missing",
#         "inventory": "📦 Inventory",
#         "your_stock": "Your Stock",
#         "no_ingredients": "No ingredients yet.",
#         "unit_tips": "Unit tips: use g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
#         "add_ingredient": "Add New Ingredient",
#         "recipes": "📖 Recipes",
#         "your_recipes": "Your Recipes",
#         "no_recipes": "No recipes yet.",
#         "save_recipe": "Save Recipe",
#         "update_recipe": "Update Recipe",
#         "delete_recipe": "Delete Recipe",
#         "feasibility": "✅ Feasibility & Shopping",
#         "create_recipes_first": "Create recipes first.",
#         "you_can_cook": "Recipe Feasibility and Shopping List",
#         "none_yet": "None yet.",
#         "all_available": "All ingredients available.",
#         "cook": "Cook",
#         "missing_something": "Missing Ingredients",
#         "all_feasible": "All recipes are feasible 🎉",
#         "add_to_shopping": "Add missing to Shopping List",
#         "shopping_list": "🛒 Shopping List",
#         "empty_list": "Your shopping list is empty.",
#         "update_inventory": "Update Inventory from Shopping List",
#         "purchased": "Inventory updated with purchased items.",
#         "select_recipes_label": "Select recipes to proceed",
#         "select_purchased": "Select purchased items",
#         "sent_to_shopping": "Missing ingredients added to the shopping list.",
#         "cook_success": "Cooked successfully.",
#         "cook_failed": "Cooking failed: {error}",
#         "adjust_recipe": "⚖️ Adjust Recipe",
#         "select_recipe": "Select Recipe",
#         "adjustment_type": "Adjustment Type",
#         "by_servings": "By Servings",
#         "by_main_ingredient": "By Main Ingredient",
#         "new_servings": "New Servings",
#         "main_ingredient": "Main Ingredient",
#         "new_quantity": "New Quantity",
#         "spice_level": "Spice Adjustment",
#         "mild": "Mild (60%)",
#         "normal": "Normal (80%)",
#         "rich": "Rich (100%)",
#         "adjusted_recipe": "Adjusted Recipe",
#         "cook_adjusted": "Cook Adjusted Recipe",
#         "add_to_shopping_adjusted": "Add Missing to Shopping List",
#         "adjusted_recipe_title": "Adjusted: {title}",
#         "no_recipe_selected": "Please select a recipe to adjust.",
#         "invalid_adjustment": "Invalid adjustment parameters.",
#         "cook_adjusted_success": "Adjusted recipe '{title}' cooked successfully.",
#         "cook_adjusted_failed": "Failed to cook adjusted recipe '{title}': {error}",
#         "not_logged_in": "You must be logged in to access this page.",
#         "error_title_required": "Recipe title is required.",
#         "error_ingredients_required": "At least one valid ingredient (with name and positive quantity) is required.",
#         "duplicate_recipe": "A recipe with this title already exists.",
#         "error_invalid_name": "Invalid ingredient name: {name}",
#         "error_invalid_unit": "Invalid unit: {unit}",
#         "error_negative_qty": "Quantity must be positive for ingredient: {name}",
#         "save_success": "Recipe '{title}' saved successfully.",
#         "update_success": "Recipe '{title}' updated successfully.",
#         "delete_success": "Recipe '{title}' deleted successfully.",
#         "save_failed": "Failed to save recipe '{title}': {error}",
#         "update_failed": "Failed to update recipe '{title}': {error}",
#         "delete_failed": "Failed to delete recipe '{title}'.",
#         "food_timeline": "🍲 Food Timeline",
#         "no_history": "No cooking history yet.",
#         "no_entries": "No entries match the filters.",
#         "congrats": "Congratulations! You have reached {stars} with {dish} 🎉",
#         "signature_dish": "Signature Dish",
#         "search_placeholder": "Search (e.g., tag:signature, week:1, day:2025-09-01)",
#         "reset_filter": "🔄 Reset filter",
#         "stats_week": "This week you cooked {count} dishes, most frequent: {dish}",
#         "db_error": "Database error: {error}",
#         "save_changes": "Save Changes",
#         "inventory_updated": "Inventory updated successfully."
#     },
#     "Vietnamese": {
#         "app_title": APP_TITLE_VI,
#         "login": "🔐 Đăng nhập",
#         "username": "Tên người dùng",
#         "password": "Mật khẩu",
#         "login_button": "Đăng nhập",
#         "register": "🆕 Đăng ký",
#         "sec_question": "Câu hỏi bảo mật (để đặt lại mật khẩu)",
#         "sec_answer": "Câu trả lời bảo mật",
#         "create_account": "Tạo tài khoản",
#         "reset_password": "♻️ Đặt lại mật khẩu",
#         "new_password": "Mật khẩu mới",
#         "reset_button": "Đặt lại mật khẩu",
#         "logout": "Đăng xuất",
#         "language": "Ngôn ngữ",
#         "title": "Tiêu đề",
#         "category": "Danh mục",
#         "instructions": "Hướng dẫn",
#         "servings": "Khẩu phần",
#         "name": "Tên",
#         "quantity": "Số lượng",
#         "unit": "Đơn vị",
#         "need": "Cần",
#         "have": "Có",
#         "missing": "Thiếu",
#         "inventory": "📦 Kho hàng",
#         "your_stock": "Kho của bạn",
#         "no_ingredients": "Chưa có nguyên liệu.",
#         "unit_tips": "Mẹo đơn vị: sử dụng g, kg, ml, l, tsp, tbsp, cup, piece, cái, pcs, lạng, chén, bát.",
#         "add_ingredient": "Thêm nguyên liệu mới",
#         "recipes": "📖 Công thức",
#         "your_recipes": "Công thức của bạn",
#         "no_recipes": "Chưa có công thức.",
#         "save_recipe": "Lưu công thức",
#         "update_recipe": "Cập nhật công thức",
#         "delete_recipe": "Xóa công thức",
#         "feasibility": "✅ Tính khả thi & Mua sắm",
#         "create_recipes_first": "Hãy tạo công thức trước.",
#         "you_can_cook": "Tính khả thi công thức và Danh sách mua sắm",
#         "none_yet": "Chưa có.",
#         "all_available": "Tất cả nguyên liệu đều có sẵn.",
#         "cook": "Nấu",
#         "missing_something": "Thiếu nguyên liệu",
#         "all_feasible": "Tất cả công thức đều khả thi 🎉",
#         "add_to_shopping": "Thêm nguyên liệu thiếu vào Danh sách mua sắm",
#         "shopping_list": "🛒 Danh sách mua sắm",
#         "empty_list": "Danh sách mua sắm của bạn trống.",
#         "update_inventory": "Cập nhật kho từ Danh sách mua sắm",
#         "purchased": "Kho hàng đã được cập nhật với các mặt hàng đã mua.",
#         "select_recipes_label": "Chọn các công thức để xử lý",
#         "select_purchased": "Chọn mục đã mua",
#         "sent_to_shopping": "Đã thêm nguyên liệu thiếu vào danh sách mua sắm.",
#         "cook_success": "Nấu ăn thành công.",
#         "cook_failed": "Nấu ăn thất bại: {error}",
#         "adjust_recipe": "⚖️ Điều chỉnh Công thức",
#         "select_recipe": "Chọn Công thức",
#         "adjustment_type": "Loại Điều chỉnh",
#         "by_servings": "Theo Khẩu phần",
#         "by_main_ingredient": "Theo Nguyên liệu Chính",
#         "new_servings": "Khẩu phần Mới",
#         "main_ingredient": "Nguyên liệu Chính",
#         "new_quantity": "Số lượng Mới",
#         "spice_level": "Mức Độ Gia vị",
#         "mild": "Nhẹ (60%)",
#         "normal": "Bình thường (80%)",
#         "rich": "Đậm (100%)",
#         "adjusted_recipe": "Công thức Đã Điều chỉnh",
#         "cook_adjusted": "Nấu Công thức Đã Điều chỉnh",
#         "add_to_shopping_adjusted": "Thêm Nguyên liệu Thiếu vào Danh sách Mua sắm",
#         "adjusted_recipe_title": "Đã điều chỉnh: {title}",
#         "no_recipe_selected": "Vui lòng chọn một công thức để điều chỉnh.",
#         "invalid_adjustment": "Tham số điều chỉnh không hợp lệ.",
#         "cook_adjusted_success": "Công thức đã điều chỉnh '{title}' được nấu thành công.",
#         "cook_adjusted_failed": "Không thể nấu công thức đã điều chỉnh '{title}': {error}",
#         "not_logged_in": "Bạn phải đăng nhập để truy cập trang này.",
#         "error_title_required": "Tiêu đề công thức là bắt buộc.",
#         "error_ingredients_required": "Cần ít nhất một nguyên liệu hợp lệ (có tên và số lượng dương).",
#         "duplicate_recipe": "Công thức với tiêu đề này đã tồn tại.",
#         "error_invalid_name": "Tên nguyên liệu không hợp lệ: {name}",
#         "error_invalid_unit": "Đơn vị không hợp lệ: {unit}",
#         "error_negative_qty": "Số lượng phải dương cho nguyên liệu: {name}",
#         "save_success": "Công thức '{title}' được lưu thành công.",
#         "update_success": "Công thức '{title}' được cập nhật thành công.",
#         "delete_success": "Công thức '{title}' được xóa thành công.",
#         "save_failed": "Không thể lưu công thức '{title}': {error}",
#         "update_failed": "Không thể cập nhật công thức '{title}': {error}",
#         "delete_failed": "Không thể xóa công thức '{title}'.",
#         "food_timeline": "🍲 Dòng thời gian món đã nấu",
#         "no_history": "Chưa có lịch sử nấu ăn.",
#         "no_entries": "Không có mục nào phù hợp với bộ lọc.",
#         "congrats": "Chúc mừng! Bạn đã lên {stars} với {dish} 🎉",
#         "signature_dish": "Món tủ",
#         "search_placeholder": "Tìm kiếm (ví dụ: tag:món tủ, tuần:1, ngày:2025-09-01)",
#         "reset_filter": "🔄 Xóa bộ lọc",
#         "stats_week": "Tuần này bạn nấu {count} món, nhiều nhất là {dish}",
#         "db_error": "Lỗi cơ sở dữ liệu: {error}",
#         "save_changes": "Lưu Thay Đổi",
#         "inventory_updated": "Kho hàng được cập nhật thành công."
#     }
# }

# # Danh sách export
# __all__ = [
#     'inject_css', 'get_text', 'current_user_id', 'initialize_session_state',
#     'topbar_account', 'inventory_page', 'recipes_page', 'feasibility_page',
#     'shopping_list_page', 'recipe_adjustment_page', 'food_timeline_page',
#     'auth_gate_tabs', 'main'
# ]

# def inject_css() -> None:
#     """Tiêm CSS tùy chỉnh để định dạng ứng dụng Streamlit."""
#     try:
#         st.markdown(
#             """
#             <style>
#                 .block-container {
#                     padding-top: 5rem;
#                     padding-bottom: 2rem;
#                     max-width: 980px;
#                 }
#                 .stTextInput > div > div > input,
#                 .stNumberInput > div > div > input,
#                 textarea {
#                     border-radius: 12px !important;
#                     border: 1px solid #e6e6e6 !important;
#                     padding: .55rem .8rem !important;
#                 }
#                 .stButton > button {
#                     background: #111 !important;
#                     color: #fff !important;
#                     border: none !important;
#                     border-radius: 14px !important;
#                     padding: .55rem 1rem !important;
#                     font-weight: 500 !important;
#                     transition: transform .12s ease, opacity .12s ease;
#                 }
#                 .stButton > button:hover {
#                     transform: translateY(-1px);
#                     opacity: .95;
#                 }
#                 table {
#                     border-collapse: collapse;
#                     width: 100%;
#                 }
#                 th, td {
#                     padding: 8px 10px;
#                     border-bottom: 1px solid #eee;
#                 }
#                 th {
#                     color: #666;
#                     font-weight: 600;
#                 }
#                 td {
#                     color: #222;
#                 }
#                 .stTabs [data-baseweb="tab-list"] {
#                     gap: .25rem;
#                     margin-top: 1rem;
#                 }
#                 .stTabs [data-baseweb="tab"] {
#                     padding: .6rem 1rem;
#                 }
#                 .streamlit-expanderHeader {
#                     font-weight: 600;
#                 }
#                 #topbar-account {
#                     margin-bottom: 1rem;
#                 }
#                 .food-card {
#                     border: 1px solid #eee;
#                     border-radius: 12px;
#                     padding: 1rem;
#                     margin-bottom: 1rem;
#                     background-color: #f9f9f9;
#                 }
#                 .dish-name {
#                     font-weight: bold;
#                     font-size: 1.2em;
#                 }
#                 .stars {
#                     font-size: 1.2em;
#                     color: #FFD700;
#                     text-align: right;
#                 }
#                 @media (max-width: 600px) {
#                     .block-container {
#                         padding-top: 4rem;
#                         padding-left: 1rem;
#                         padding-right: 1rem;
#                     }
#                     .stButton > button {
#                         width: 100%;
#                         margin-bottom: 0.5rem;
#                     }
#                     .stTabs [data-baseweb="tab-list"] {
#                         margin-top: 0.5rem;
#                     }
#                 }
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )
#     except Exception as e:
#         logger.error(f"Lỗi tiêm CSS: {e}")
#         st.error("Không thể áp dụng kiểu dáng tùy chỉnh. Tiếp tục với kiểu mặc định.")

# def get_text(key: str, **kwargs) -> str:
#     """Truy xuất văn bản đa ngôn ngữ với format an toàn."""
#     lang = st.session_state.get("language", "English")
#     template = TEXT.get(lang, TEXT["English"]).get(key, key)
#     if kwargs:
#         try:
#             return template.format(**kwargs)
#         except Exception as e:
#             logger.warning(f"i18n fallback cho key='{key}': {e}")
#             return template
#     return template

# def current_user_id() -> Optional[int]:
#     """Lấy ID người dùng hiện tại từ session_state."""
#     return st.session_state.get("user_id")

# def initialize_session_state() -> None:
#     """Khởi tạo trạng thái phiên với các giá trị mặc định."""
#     defaults = {
#         "user_id": None,
#         "username": None,
#         "language": "English",
#         "editing_recipe_id": None,
#         "recipe_form_data": {
#             "title": "",
#             "category": "",
#             "instructions": "",
#             "is_signature": False,
#             "servings": 1.0,
#             "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#         },
#         "shopping_list_data": [],
#         "adjusted_recipe": None,
#         "search_value": ""
#     }
#     for key, value in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = value

# def topbar_account() -> None:
#     """Hiển thị thanh trên cùng với tên người dùng, chọn ngôn ngữ và nút đăng xuất."""
#     user_id = current_user_id()
#     if not user_id:
#         return
#     with st.container():
#         st.markdown('<div id="topbar-account">', unsafe_allow_html=True)
#         col1, col2, col3 = st.columns([3, 1, 1])
#         with col1:
#             st.write(f"{get_text('username')}: {html.escape(st.session_state.get('username', 'Unknown'))}")
#         with col2:
#             st.selectbox(
#                 get_text("language"),
#                 ["English", "Vietnamese"],
#                 index=0 if st.session_state.get("language", "English") == "English" else 1,
#                 key="language_selector",
#                 on_change=lambda: st.session_state.update({"language": st.session_state.language_selector})
#             )
#         with col3:
#             if st.button(get_text("logout")):
#                 st.session_state.clear()
#                 initialize_session_state()
#                 logger.info(f"User {st.session_state.get('username', 'Unknown')} logged out")
#                 st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)

# def calculate_stars(count: int, is_signature: bool) -> int:
#     """Tính số sao dựa trên số lần nấu và trạng thái món tủ."""
#     if not isinstance(count, int) or count < 0:
#         return 0
#     thresholds = [(15, 5), (8, 4), (5, 3), (3, 2), (1, 1)]
#     return 5 if is_signature else next((stars for threshold, stars in thresholds if count >= threshold), 0)

# # Helper functions
# def _norm_name(name: str) -> str:
#     """Chuẩn hóa tên nguyên liệu để so sánh."""
#     return (name or "").strip().lower()

# def _norm_unit(unit: str) -> str:
#     """Chuẩn hóa đơn vị để so sánh."""
#     return (unit or "").strip().lower()

# def _inventory_map(user_id: int) -> Dict[Tuple[str, str], dict]:
#     """Tạo bản đồ kho dựa trên tên và đơn vị chuẩn hóa."""
#     return {
#         (_norm_name(item["name"]), _norm_unit(item["unit"])): item
#         for item in DatabaseManager.list_inventory(user_id)
#         if item.get("name") and item.get("unit")
#     }

# def validate_ingredients(recipe: Dict, inventory_map: Dict[Tuple[str, str], dict]) -> Tuple[bool, Optional[str]]:
#     """Kiểm tra tính hợp lệ và khả thi của các nguyên liệu trong công thức."""
#     if not recipe.get("ingredients"):
#         return False, get_text("error_ingredients_required")
    
#     for ing in recipe.get("ingredients", []):
#         name = _norm_name(ing.get("name", ""))
#         unit = _norm_unit(ing.get("unit", ""))
#         qty = float(ing.get("quantity", 0.0))
        
#         if not name or qty <= 0:
#             return False, get_text("error_ingredients_required")
#         if not DatabaseManager.validate_name(ing.get("name", "")):
#             return False, get_text("error_invalid_name").format(name=ing.get("name"))
#         if unit not in [_norm_unit(u) for u in VALID_UNITS]:
#             return False, get_text("error_invalid_unit").format(unit=ing.get("unit"))
        
#         key = (name, unit)
#         inv_item = inventory_map.get(key)
#         if not inv_item:
#             return False, f"Ingredient {ing.get('name')} not found in inventory"
#         if inv_item["unit"] != ing.get("unit"):
#             return False, f"Unit mismatch for {ing.get('name')}: expected {ing.get('unit')}, found {inv_item['unit']}"
#         if inv_item["quantity"] < qty:
#             return False, f"Insufficient quantity for {ing.get('name')}: need {qty}, have {inv_item['quantity']}"
    
#     return True, None

# def recipe_feasibility(recipe: Dict, user_id: int) -> Tuple[bool, List[Dict]]:
#     """Kiểm tra tính khả thi của công thức dựa trên kho."""
#     inv_map = _inventory_map(user_id)
#     shorts = []
#     feasible = True
    
#     for ing in recipe.get("ingredients", []):
#         name = _norm_name(ing.get("name", ""))
#         unit = _norm_unit(ing.get("unit", ""))
#         qty = float(ing.get("quantity", 0.0))
#         key = (name, unit)
#         inv_item = inv_map.get(key, {})
#         have_qty = float(inv_item.get("quantity", 0.0))
#         missing = max(0.0, qty - have_qty)
        
#         if missing > 1e-9 or not inv_item:
#             feasible = False
#             shorts.append({
#                 "name": ing.get("name", ""),
#                 "needed_qty": qty,
#                 "have_qty": have_qty,
#                 "needed_unit": ing.get("unit", ""),
#                 "have_unit": inv_item.get("unit", "") if inv_item else "",
#                 "missing_qty_disp": missing,
#                 "missing_unit_disp": ing.get("unit", "")
#             })
    
#     return feasible, shorts

# def consume_ingredients_for_recipe(recipe: Dict, user_id: int) -> Tuple[bool, str]:
#     """Tiêu thụ nguyên liệu từ kho nếu công thức khả thi, sử dụng giao dịch nguyên tử."""
#     inv_map = _inventory_map(user_id)
#     is_valid, error = validate_ingredients(recipe, inv_map)
#     if not is_valid:
#         logger.warning(f"Validation failed for recipe {recipe.get('title', 'Unknown')}: {error}")
#         return False, get_text("cook_failed").format(error=error)
    
#     try:
#         with TransactionContext(DatabaseManager, user_id):
#             for ing in recipe.get("ingredients", []):
#                 name = _norm_name(ing.get("name", ""))
#                 unit = _norm_unit(ing.get("unit", ""))
#                 qty = float(ing.get("quantity", 0.0))
#                 key = (name, unit)
#                 inv_item = inv_map.get(key)
                
#                 if not inv_item:
#                     raise ValueError(f"Ingredient {ing.get('name')} not found in inventory")
#                 if inv_item["unit"] != ing.get("unit"):
#                     raise ValueError(f"Unit mismatch for {ing.get('name')}")
#                 if inv_item["quantity"] < qty:
#                     raise ValueError(f"Insufficient quantity for {ing.get('name')}")
                
#                 new_qty = max(0.0, inv_item["quantity"] - qty)
#                 DatabaseManager.update_inventory_item(user_id, inv_item["id"], inv_item["name"], new_qty, inv_item["unit"])
        
#         logger.info(f"Successfully consumed ingredients for recipe {recipe.get('title', 'Unknown')}")
#         return True, get_text("cook_success")
    
#     except Exception as e:
#         logger.error(f"Failed to consume ingredients for recipe {recipe.get('title', 'Unknown')}: {str(e)}")
#         return False, get_text("cook_failed").format(error=str(e))

# # Transaction Context for atomic operations
# class TransactionContext:
#     def __init__(self, db_manager: 'DatabaseManager', user_id: int):
#         self.db_manager = db_manager
#         self.user_id = user_id
#         self.original_inventory = None
    
#     def __enter__(self):
#         """Lưu trạng thái kho trước khi thực hiện giao dịch."""
#         self.original_inventory = self.db_manager.list_inventory(self.user_id).copy()
#         return self
    
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         """Khôi phục trạng thái kho nếu có lỗi."""
#         if exc_type is not None:
#             self.db_manager._inventory[self.user_id] = self.original_inventory
#             logger.error(f"Transaction rolled back for user {self.user_id}: {exc_val}")
#         else:
#             logger.debug(f"Transaction committed for user {self.user_id}")

# # Database Manager
# class DatabaseManager:
#     _users: Dict[str, Dict] = {}
#     _next_user_id: int = 1
#     _inventory: Dict[int, List[Dict]] = {}
#     _recipes: Dict[int, List[Dict]] = {}
#     _cooked_history: Dict[int, List[Dict]] = {}
#     _cooked_count: Dict[Tuple[int, int], int] = {}

#     @staticmethod
#     def validate_name(name: str) -> bool:
#         """Kiểm tra tên nguyên liệu hợp lệ."""
#         return bool(name.strip() and re.match(r'^[\w\s\-\']+$', name))

#     @staticmethod
#     def normalize_name(name: str) -> str:
#         """Chuẩn hóa tên để so sánh."""
#         return _norm_name(name)

#     @classmethod
#     def verify_login(cls, username: str, password: str) -> Optional[int]:
#         """Xác minh đăng nhập."""
#         if not username or not password or len(password) < 8:
#             return None
#         user = cls._users.get(username)
#         if user and user["password_hash"] == hashlib.sha256(password.encode()).hexdigest():
#             return user["id"]
#         return None

#     @classmethod
#     def create_user(cls, username: str, password: str, sec_question: str, sec_answer: str) -> Tuple[bool, str]:
#         """Tạo người dùng mới."""
#         if not all([username.strip(), password.strip(), sec_question.strip(), sec_answer.strip()]):
#             return False, "All fields required."
#         if len(password) < 8:
#             return False, "Password must be at least 8 characters."
#         if not cls.validate_name(username):
#             return False, get_text("error_invalid_name").format(name=username)
#         if username in cls._users:
#             return False, "Username already exists."
#         user_id = cls._next_user_id
#         cls._users[username] = {
#             "id": user_id,
#             "password_hash": hashlib.sha256(password.encode()).hexdigest(),
#             "sec_question": sec_question,
#             "sec_answer_hash": hashlib.sha256(sec_answer.encode()).hexdigest()
#         }
#         cls._next_user_id += 1
#         cls._inventory[user_id] = []
#         cls._recipes[user_id] = []
#         cls._cooked_history[user_id] = []
#         return True, "User created successfully."

#     @classmethod
#     def reset_password(cls, username: str, sec_answer: str, new_password: str) -> bool:
#         """Đặt lại mật khẩu."""
#         if not all([username.strip(), sec_answer.strip(), new_password.strip()]):
#             return False
#         if len(new_password) < 8:
#             return False
#         user = cls._users.get(username)
#         if not user:
#             return False
#         if user["sec_answer_hash"] == hashlib.sha256(sec_answer.encode()).hexdigest():
#             user["password_hash"] = hashlib.sha256(new_password.encode()).hexdigest()
#             return True
#         return False

#     @classmethod
#     def list_inventory(cls, user_id: int) -> List[Dict]:
#         """Liệt kê kho của người dùng."""
#         return cls._inventory.get(user_id, [])

#     @classmethod
#     def upsert_inventory(cls, user_id: int, name: str, quantity: float, unit: str) -> None:
#         """Thêm hoặc cập nhật item trong kho (cập nhật bằng cách cộng quantity nếu tồn tại)."""
#         inv = cls._inventory.setdefault(user_id, [])
#         for item in inv:
#             if _norm_name(item["name"]) == _norm_name(name) and _norm_unit(item["unit"]) == _norm_unit(unit):
#                 item["quantity"] = max(0.0, item["quantity"] + quantity)
#                 return
#         inv.append({"id": len(inv) + 1, "name": name, "quantity": max(0.0, quantity), "unit": unit})

#     @classmethod
#     def update_inventory_item(cls, user_id: int, item_id: int, name: str, quantity: float, unit: str) -> bool:
#         """Cập nhật item cụ thể trong kho theo ID."""
#         items = cls._inventory.get(user_id, [])
#         for item in items:
#             if item.get("id") == item_id:
#                 if not cls.validate_name(name):
#                     logger.error(f"Invalid name for inventory item: {name}")
#                     return False
#                 if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                     logger.error(f"Invalid unit for inventory item: {unit}")
#                     return False
#                 if quantity < 0:
#                     logger.error(f"Negative quantity for inventory item: {name}")
#                     return False
#                 item.update({"name": name, "quantity": max(0.0, quantity), "unit": unit})
#                 return True
#         logger.error(f"Inventory item not found: id={item_id}, user_id={user_id}")
#         return False

#     @classmethod
#     def delete_inventory(cls, user_id: int, item_id: int) -> None:
#         """Xóa item khỏi kho theo ID."""
#         items = cls._inventory.get(user_id, [])
#         for i, item in enumerate(items):
#             if item.get("id") == item_id:
#                 del items[i]
#                 return

#     @classmethod
#     def list_recipes(cls, user_id: int) -> List[Dict]:
#         """Liệt kê công thức của người dùng."""
#         return cls._recipes.get(user_id, [])

#     @classmethod
#     def create_recipe(cls, user_id: int, title: str, category: str, instructions: str, 
#                       ingredients: List[Dict], recipe_id: Optional[int] = None, is_signature: bool = False) -> Tuple[bool, str]:
#         """Tạo hoặc cập nhật công thức."""
#         if not title.strip():
#             return False, get_text("error_title_required")
#         if not any(ing["name"].strip() and ing["quantity"] > 0 for ing in ingredients):
#             return False, get_text("error_ingredients_required")
#         recipes = cls._recipes.setdefault(user_id, [])
#         if any(r["title"] == title and r.get("id") != recipe_id for r in recipes):
#             return False, get_text("duplicate_recipe")
#         recipe = {
#             "id": recipe_id if recipe_id else len(recipes) + 1,
#             "title": title,
#             "category": category,
#             "instructions": instructions,
#             "servings": 1.0,
#             "is_signature": is_signature,
#             "ingredients": ingredients
#         }
#         if recipe_id:
#             for i, r in enumerate(recipes):
#                 if r["id"] == recipe_id:
#                     recipes[i] = recipe
#                     return True, get_text("update_success").format(title=title)
#         recipes.append(recipe)
#         return True, get_text("save_success").format(title=title)

#     @classmethod
#     def delete_recipe(cls, user_id: int, recipe_id: int) -> bool:
#         """Xóa công thức."""
#         recipes = cls._recipes.get(user_id, [])
#         for i, r in enumerate(recipes):
#             if r["id"] == recipe_id:
#                 del recipes[i]
#                 return True
#         return False

#     @classmethod
#     def log_cooked_recipe(cls, user_id: int, recipe_id: int) -> None:
#         """Ghi log công thức đã nấu."""
#         history = cls._cooked_history.setdefault(user_id, [])
#         history.append({"recipe_id": recipe_id, "cooked_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
#         cls._cooked_count[(user_id, recipe_id)] = cls._cooked_count.get((user_id, recipe_id), 0) + 1

#     @classmethod
#     def list_cooked_history(cls, user_id: int) -> List[Dict]:
#         """Liệt kê lịch sử nấu ăn."""
#         return cls._cooked_history.get(user_id, [])

#     @classmethod
#     def get_cooked_count(cls, user_id: int, recipe_id: int) -> int:
#         """Lấy số lần nấu công thức."""
#         return cls._cooked_count.get((user_id, recipe_id), 0)

# # Khởi tạo user mẫu
# DatabaseManager._users["admin1234"] = {
#     "id": 1,
#     "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
#     "sec_question": "What is your pet's name?",
#     "sec_answer_hash": hashlib.sha256("dog".encode()).hexdigest()
# }
# DatabaseManager._inventory[1] = []
# DatabaseManager._recipes[1] = []
# DatabaseManager._cooked_history[1] = []
# DatabaseManager._next_user_id = 2

# def inventory_page() -> None:
#     """Hiển thị và quản lý kho nguyên liệu."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except Exception as e:
#         logger.error(f"Lỗi tải kho cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     st.header(get_text("inventory"))
#     st.subheader(get_text("your_stock"))
#     st.caption(get_text("unit_tips"))

#     with st.expander(get_text("add_ingredient")):
#         with st.form(key="add_inventory_form"):
#             col1, col2, col3 = st.columns([2, 1, 1])
#             with col1:
#                 ingredient_name = st.text_input(get_text("name"), placeholder=get_text("e.g., chicken"), key="new_ingredient_name")
#             with col2:
#                 quantity = st.number_input(get_text("quantity"), min_value=0.0, step=0.1, value=0.0, key="new_quantity")
#             with col3:
#                 unit = st.selectbox(get_text("unit"), options=VALID_UNITS, key="new_unit")
#             if st.form_submit_button(get_text("add_ingredient")):
#                 if not ingredient_name.strip() or quantity < 0:
#                     st.error(get_text("error_ingredients_required"))
#                 elif not DatabaseManager.validate_name(ingredient_name):
#                     st.error(get_text("error_invalid_name").format(name=ingredient_name))
#                 elif not _norm_unit(unit) in [_norm_unit(u) for u in VALID_UNITS]:
#                     st.error(get_text("error_invalid_unit").format(unit=unit))
#                 else:
#                     try:
#                         DatabaseManager.upsert_inventory(user_id, ingredient_name.strip(), quantity, unit)
#                         st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                         st.success(get_text("save_success").format(title=ingredient_name))
#                         st.rerun()
#                     except Exception as e:
#                         logger.error(f"Lỗi thêm nguyên liệu {ingredient_name}: {e}")
#                         st.error(get_text("db_error").format(error=e))

#     edited_data = st.data_editor(
#         inventory,
#         column_config={
#             "id": None,
#             "name": st.column_config.TextColumn(get_text("name"), required=True),
#             "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
#             "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#         },
#         num_rows="dynamic",
#         key=f"inventory_editor_{user_id}",
#         hide_index=True
#     )

#     if st.button(get_text("save_changes")):
#         errors = []
#         for item in edited_data:
#             name = item.get("name", "").strip()
#             quantity = item.get("quantity")
#             unit = item.get("unit", "")
#             if not name or not isinstance(quantity, (int, float)) or quantity < 0 or not unit:
#                 errors.append(get_text("error_ingredients_required"))
#                 continue
#             if not DatabaseManager.validate_name(name):
#                 errors.append(get_text("error_invalid_name").format(name=name))
#                 continue
#             if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                 errors.append(get_text("error_invalid_unit").format(unit=unit))
#                 continue
#         if errors:
#             for error in errors:
#                 st.error(error)
#         else:
#             try:
#                 with TransactionContext(DatabaseManager, user_id):
#                     for item in edited_data:
#                         if "id" in item:
#                             if not DatabaseManager.update_inventory_item(user_id, item["id"], item["name"], item["quantity"], item["unit"]):
#                                 raise ValueError(f"Failed to update inventory item {item['name']}")
#                         else:
#                             DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"])
#                     old_ids = {item.get("id") for item in inventory if "id" in item}
#                     edited_ids = {item.get("id") for item in edited_data if "id" in item}
#                     deleted_ids = old_ids - edited_ids
#                     for item_id in deleted_ids:
#                         DatabaseManager.delete_inventory(user_id, item_id)
#                 st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                 st.success(get_text("inventory_updated"))
#                 st.rerun()
#             except Exception as e:
#                 logger.error(f"Lỗi cập nhật kho: {e}")
#                 st.error(get_text("db_error").format(error=e))

#     if not inventory:
#         st.info(get_text("no_ingredients"))

# def recipes_page() -> None:
#     """Hiển thị và quản lý công thức của người dùng."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#     except Exception as e:
#         logger.error(f"Lỗi tải công thức cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     st.header(get_text("recipes"))
#     st.subheader(get_text("your_recipes"))
#     st.caption(get_text("unit_tips"))

#     if not recipes:
#         st.info(get_text("no_recipes"))

#     form_data = st.session_state.recipe_form_data
#     recipe_id = st.session_state.get("editing_recipe_id")

#     with st.form(key="recipe_form"):
#         title = st.text_input(get_text("title"), value=form_data["title"], key="recipe_title")
#         category = st.text_input(get_text("category"), value=form_data["category"], key="recipe_category")
#         instructions = st.text_area(get_text("instructions"), value=form_data["instructions"], key="recipe_instructions")
#         is_signature = st.checkbox(get_text("signature_dish"), value=form_data["is_signature"], key="recipe_is_signature")
#         ingredients_data = st.data_editor(
#             form_data["ingredients"],
#             column_config={
#                 "name": st.column_config.TextColumn(get_text("name"), required=True),
#                 "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
#                 "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#                 "is_spice": st.column_config.CheckboxColumn("Spice", default=False)
#             },
#             num_rows="dynamic",
#             key="ingredients_editor",
#             hide_index=True
#         )

#         submit_label = get_text("update_recipe") if recipe_id else get_text("save_recipe")
#         if st.form_submit_button(submit_label):
#             if not title.strip():
#                 st.error(get_text("error_title_required"))
#                 return
#             valid_ingredients = [
#                 ing for ing in ingredients_data
#                 if DatabaseManager.normalize_name(ing.get("name", "")).strip() and
#                 isinstance(ing.get("quantity"), (int, float)) and ing["quantity"] > 0 and
#                 _norm_unit(ing.get("unit", "")) in [_norm_unit(u) for u in VALID_UNITS]
#             ]
#             if not valid_ingredients:
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             existing_recipe = next((r for r in recipes if r.get("title") == title.strip() and r.get("id") != recipe_id), None)
#             if existing_recipe:
#                 st.error(get_text("duplicate_recipe"))
#                 return
#             for ing in valid_ingredients:
#                 if not DatabaseManager.validate_name(ing["name"]):
#                     st.error(get_text("error_invalid_name").format(name=ing["name"]))
#                     return
#                 if not _norm_unit(ing["unit"]) in [_norm_unit(u) for u in VALID_UNITS]:
#                     st.error(get_text("error_invalid_unit").format(unit=ing["unit"]))
#                     return
#                 if ing["quantity"] <= 0:
#                     st.error(get_text("error_negative_qty").format(name=ing["name"]))
#                     return
#             try:
#                 success, message = DatabaseManager.create_recipe(
#                     user_id, title.strip(), category.strip(), instructions.strip(), 
#                     valid_ingredients, recipe_id, is_signature
#                 )
#                 if success:
#                     st.success(message)
#                     st.session_state.recipe_form_data = {
#                         "title": "",
#                         "category": "",
#                         "instructions": "",
#                         "is_signature": False,
#                         "servings": 1.0,
#                         "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#                     }
#                     st.session_state.editing_recipe_id = None
#                     st.rerun()
#                 else:
#                     st.error(message)
#             except Exception as e:
#                 logger.error(f"Lỗi lưu công thức {title}: {e}")
#                 st.error(get_text("save_failed").format(title=title, error=str(e)))

#     if recipes:
#         for recipe in recipes:
#             signature_text = f" - {get_text('signature_dish')}" if recipe.get("is_signature") else ""
#             with st.expander(f"{html.escape(recipe.get('title', 'Untitled'))} ({html.escape(recipe.get('category', '-'))}) {signature_text}"):
#                 st.write(f"**{get_text('instructions')}:** {html.escape(recipe.get('instructions', ''))}")
#                 st.table([
#                     {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
#                      get_text("unit"): ing["unit"], "Spice": "Yes" if ing.get("is_spice") else "No"}
#                     for ing in recipe.get("ingredients", [])
#                 ])
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button(get_text("update_recipe"), key=f"edit_{recipe.get('id')}"):
#                         st.session_state.editing_recipe_id = recipe["id"]
#                         st.session_state.recipe_form_data = {
#                             "title": recipe["title"],
#                             "category": recipe["category"],
#                             "instructions": recipe["instructions"],
#                             "is_signature": recipe.get("is_signature", False),
#                             "servings": recipe.get("servings", 1.0),
#                             "ingredients": [
#                                 {"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": ing.get("is_spice", False)}
#                                 for ing in recipe.get("ingredients", [])
#                             ]
#                         }
#                         st.rerun()
#                 with col2:
#                     if st.button(get_text("delete_recipe"), key=f"delete_{recipe.get('id')}"):
#                         try:
#                             if DatabaseManager.delete_recipe(user_id, recipe["id"]):
#                                 st.success(get_text("delete_success").format(title=recipe["title"]))
#                                 st.rerun()
#                             else:
#                                 st.error(get_text("delete_failed").format(title=recipe["title"]))
#                         except Exception as e:
#                             logger.error(f"Lỗi xóa công thức {recipe['title']}: {e}")
#                             st.error(get_text("delete_failed").format(title=recipe["title"]))

# def feasibility_page() -> None:
#     """Hiển thị tính khả thi của công thức và tùy chọn danh sách mua sắm."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except Exception as e:
#         logger.error(f"Lỗi tải dữ liệu cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     if not recipes:
#         st.info(get_text("create_recipes_first"))
#         return

#     st.header(get_text("feasibility"))
#     st.subheader(get_text("you_can_cook"))

#     recipe_results = [
#         {"recipe": r, "feasible": feasible, "shorts": shorts}
#         for r in recipes
#         for feasible, shorts in [recipe_feasibility(r, user_id)]
#     ]

#     if not recipe_results:
#         st.info(get_text("none_yet"))
#         return

#     if all(r["feasible"] for r in recipe_results):
#         st.success(get_text("all_feasible"))

#     selected_titles = st.multiselect(
#         get_text("select_recipes_label"),
#         [r["recipe"]["title"] for r in recipe_results],
#         format_func=lambda t: f"{t} {'✅' if next((r for r in recipe_results if r['recipe']['title'] == t), {}).get('feasible', False) else '❌'}"
#     )

#     selected_missing = []
#     for result in [r for r in recipe_results if r["recipe"]["title"] in selected_titles]:
#         st.markdown(f"#### {html.escape(result['recipe'].get('title', 'Untitled'))}")
#         if result["feasible"]:
#             st.success(get_text("all_available"))
#             if st.button(get_text("cook"), key=f"cook_{result['recipe'].get('id')}"):
#                 success, message = consume_ingredients_for_recipe(result["recipe"], user_id)
#                 if success:
#                     DatabaseManager.log_cooked_recipe(user_id, result["recipe"]["id"])
#                     count = DatabaseManager.get_cooked_count(user_id, result["recipe"]["id"])
#                     stars = calculate_stars(count, result["recipe"].get("is_signature", False))
#                     if stars > calculate_stars(count - 1, result["recipe"].get("is_signature", False)):
#                         st.success(get_text("congrats").format(stars="⭐" * stars, dish=result["recipe"]["title"]))
#                     st.success(message)
#                     st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                     st.rerun()
#                 else:
#                     st.error(message)
#                     _, shorts = recipe_feasibility(result["recipe"], user_id)
#                     if shorts:
#                         st.table([
#                             {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
#                              get_text("have"): f"{s['have_qty']} {s['have_unit']}",
#                              get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
#                             for s in shorts
#                         ])
#         else:
#             st.warning(get_text("missing_something"))
#             st.table([
#                 {get_text("name"): s["name"], get_text("need"): s["needed_qty"], get_text("have"): s["have_qty"],
#                  get_text("unit"): s["needed_unit"], get_text("missing"): s["missing_qty_disp"]}
#                 for s in result["shorts"]
#             ])
#             selected_missing.extend(result["shorts"])

#     if selected_missing and st.button(get_text("add_to_shopping")):
#         agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
#         for s in selected_missing:
#             key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
#             agg_missing[key]["name"] = s["name"]
#             agg_missing[key]["quantity"] += s["missing_qty_disp"]
#             agg_missing[key]["unit"] = s["missing_unit_disp"]
#         st.session_state["shopping_list_data"] = list(agg_missing.values())
#         st.success(get_text("sent_to_shopping"))
#         st.rerun()

# def shopping_list_page() -> None:
#     """Quản lý danh sách mua sắm và cập nhật kho."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except Exception as e:
#         logger.error(f"Lỗi tải kho cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     shopping_list = st.session_state.get("shopping_list_data", [])
#     st.header(get_text("shopping_list"))
#     if not shopping_list:
#         st.info(get_text("empty_list"))
#         return

#     valid_shopping_list = []
#     for item in shopping_list:
#         if (
#             isinstance(item, dict) and
#             item.get("name") and isinstance(item.get("name"), str) and
#             isinstance(item.get("quantity"), (int, float)) and item["quantity"] >= 0 and
#             item.get("unit") and _norm_unit(item["unit"]) in [_norm_unit(u) for u in VALID_UNITS]
#         ):
#             valid_shopping_list.append(item)
#         else:
#             logger.warning(f"Invalid shopping list item: {item}")
#     shopping_list = valid_shopping_list
#     st.session_state["shopping_list_data"] = shopping_list

#     shopping_data = st.data_editor(
#         shopping_list,
#         column_config={
#             "name": st.column_config.TextColumn(get_text("name"), required=True),
#             "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
#             "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#         },
#         num_rows="dynamic",
#         key="shopping_list_editor",
#         hide_index=True
#     )

#     st.session_state["shopping_list_data"] = shopping_data
#     purchased_labels = [f"{item['name']} ({item['unit']})" for item in shopping_data if item.get("name") and item.get("unit")]
#     purchased_names = st.multiselect(get_text("select_purchased"), options=purchased_labels)

#     if st.button(get_text("update_inventory")):
#         try:
#             with TransactionContext(DatabaseManager, user_id):
#                 for item in shopping_data:
#                     item_label = f"{item['name']} ({item['unit']})"
#                     if item_label in purchased_names:
#                         DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"])
#                 st.session_state["shopping_list_data"] = [
#                     item for item in shopping_data if f"{item['name']} ({item['unit']})" not in purchased_names
#                 ]
#             st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#             st.success(get_text("purchased"))
#             st.rerun()
#         except Exception as e:
#             logger.error(f"Lỗi cập nhật kho từ danh sách mua sắm: {e}")
#             st.error(get_text("db_error").format(error=e))

# def recipe_adjustment_page() -> None:
#     """Điều chỉnh công thức dựa trên khẩu phần hoặc nguyên liệu chính."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except Exception as e:
#         logger.error(f"Lỗi tải dữ liệu cho điều chỉnh của người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     st.header(get_text("adjust_recipe"))
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#     except Exception as e:
#         logger.error(f"Lỗi tải công thức cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     if not recipes:
#         st.info(get_text("no_recipes"))
#         return

#     selected_recipe_title = st.selectbox(get_text("select_recipe"), [r.get("title") for r in recipes])
#     if not selected_recipe_title:
#         st.warning(get_text("no_recipe_selected"))
#         return

#     recipe = next(r for r in recipes if r.get("title") == selected_recipe_title)
#     adjustment_type = st.radio(get_text("adjustment_type"), [get_text("by_servings"), get_text("by_main_ingredient")])
#     adjustment_ratio = 1.0

#     if adjustment_type == get_text("by_servings"):
#         base_servings = float(recipe.get("servings", 1.0))
#         new_servings = st.number_input(get_text("new_servings"), min_value=0.1, step=0.1, value=base_servings)
#         adjustment_ratio = new_servings / base_servings if base_servings > 0 else 1.0
#     else:
#         main_ingredients = [ing for ing in recipe.get("ingredients", []) if not ing.get("is_spice")]
#         if not main_ingredients:
#             st.error(get_text("error_ingredients_required"))
#             return
#         main_ingredient = st.selectbox(get_text("main_ingredient"), [ing.get("name") for ing in main_ingredients])
#         selected_ing = next(ing for ing in main_ingredients if ing.get("name") == main_ingredient)
#         base_qty = float(selected_ing.get("quantity", 1.0))
#         new_quantity = st.number_input(get_text("new_quantity"), min_value=0.0, step=0.1, value=base_qty)
#         adjustment_ratio = new_quantity / base_qty if base_qty > 0 else 1.0

#     spice_display_to_key = {
#         get_text("mild"): "mild",
#         get_text("normal"): "normal",
#         get_text("rich"): "rich"
#     }
#     spice_level = st.radio(get_text("spice_level"), [get_text("mild"), get_text("normal"), get_text("rich")])
#     spice_key = spice_display_to_key.get(spice_level, "normal")
#     spice_factor = {"mild": 0.6, "normal": 0.8, "rich": 1.0}[spice_key]

#     adjusted_recipe = {
#         "id": recipe.get("id"),
#         "title": get_text("adjusted_recipe_title").format(title=recipe.get("title")),
#         "category": recipe.get("category"),
#         "instructions": recipe.get("instructions"),
#         "servings": (recipe.get("servings", 1.0) * adjustment_ratio) if adjustment_type == get_text("by_servings") else recipe.get("servings", 1.0),
#         "ingredients": [],
#         "origin_id": recipe.get("id"),
#         "tag": "adjusted"
#     }

#     for ing in recipe.get("ingredients", []):
#         new_qty = max(0.0, float(ing.get("quantity", 0.0)) * adjustment_ratio * (spice_factor if ing.get("is_spice") else 1.0))
#         adjusted_recipe["ingredients"].append({
#             "name": ing.get("name"),
#             "quantity": new_qty,
#             "unit": ing.get("unit"),
#             "is_spice": ing.get("is_spice", False)
#         })

#     st.session_state["adjusted_recipe"] = adjusted_recipe
#     st.subheader(get_text("adjusted_recipe"))
#     st.write(f"**{get_text('title')}:** {html.escape(adjusted_recipe['title'])}")
#     st.write(f"**{get_text('category')}:** {html.escape(adjusted_recipe.get('category', ''))}")
#     st.write(f"**{get_text('servings')}:** {float(adjusted_recipe.get('servings', 0.0)):.2f}")
#     st.write(f"**{get_text('instructions')}:** {html.escape(adjusted_recipe.get('instructions', ''))}")
#     st.table([
#         {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
#          get_text("unit"): ing["unit"], "Spice": "Yes" if ing["is_spice"] else "No"}
#         for ing in adjusted_recipe["ingredients"]
#     ])

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button(get_text("cook_adjusted")):
#             feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
#             success, message = consume_ingredients_for_recipe(adjusted_recipe, user_id)
#             if success:
#                 DatabaseManager.log_cooked_recipe(user_id, adjusted_recipe["origin_id"])
#                 count = DatabaseManager.get_cooked_count(user_id, adjusted_recipe["origin_id"])
#                 stars = calculate_stars(count, recipe.get("is_signature", False))
#                 if stars > calculate_stars(count - 1, recipe.get("is_signature", False)):
#                     st.success(get_text("congrats").format(stars="⭐" * stars, dish=adjusted_recipe["title"]))
#                 st.success(get_text("cook_adjusted_success").format(title=adjusted_recipe["title"]))
#                 st.session_state.pop("adjusted_recipe", None)
#                 st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                 st.rerun()
#             else:
#                 st.error(get_text("cook_adjusted_failed").format(title=adjusted_recipe["title"], error=message.split(": ")[-1]))
#                 if shorts:
#                     st.table([
#                         {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
#                          get_text("have"): f"{s['have_qty']} {s['have_unit']}",
#                          get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
#                         for s in shorts
#                     ])

#     with col2:
#         if st.button(get_text("add_to_shopping_adjusted")):
#             feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
#             if not feasible:
#                 agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
#                 for s in shorts:
#                     key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
#                     agg_missing[key]["name"] = s["name"]
#                     agg_missing[key]["quantity"] += s["missing_qty_disp"]
#                     agg_missing[key]["unit"] = s["missing_unit_disp"]
#                 st.session_state["shopping_list_data"] = st.session_state.get("shopping_list_data", []) + list(agg_missing.values())
#                 st.success(get_text("sent_to_shopping"))
#                 st.rerun()

# def food_timeline_page() -> None:
#     """Hiển thị lịch sử nấu ăn dưới dạng dòng thời gian."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         history = DatabaseManager.list_cooked_history(user_id)
#         recipes = {r["id"]: r for r in DatabaseManager.list_recipes(user_id)}
#         st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#     except Exception as e:
#         logger.error(f"Lỗi tải dữ liệu dòng thời gian: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     st.header(get_text("food_timeline"))
#     if not history:
#         st.info(get_text("no_history"))
#         return

#     recipe_counts = defaultdict(int)
#     for h in history:
#         recipe_counts[h["recipe_id"]] += 1

#     enriched = [
#         {
#             "date": h["cooked_date"],
#             "name": recipes[h["recipe_id"]]["title"],
#             "stars": calculate_stars(recipe_counts[h["recipe_id"]], recipes[h["recipe_id"]].get("is_signature", False)),
#             "recipe_id": h["recipe_id"],
#             "index": idx
#         }
#         for idx, h in enumerate(history) if h["recipe_id"] in recipes
#     ]

#     with st.form(key="timeline_search_form"):
#         search_query = st.text_input(get_text("search_placeholder"), value=st.session_state.get("search_value", ""), key="timeline_search_input")
#         if st.form_submit_button(get_text("reset_filter")):
#             st.session_state.search_value = ""
#             st.rerun()

#     tag_filter, week_filter, day_filter = None, None, None
#     if search_query:
#         if search_query.startswith("tag:"):
#             tag_filter = search_query[4:].strip().lower()
#         elif search_query.startswith(("tuần:", "week:")):
#             week_filter = search_query.split(":")[1].strip()
#         elif search_query.startswith(("ngày:", "day:")):
#             day_filter = search_query.split(":")[1].strip()
#         else:
#             keyword = search_query.lower()
#         st.session_state.search_value = search_query

#     filtered = enriched
#     if tag_filter:
#         filtered = [e for e in filtered if (tag_filter in ["signature", "món tủ"] and e["stars"] == 5) or (tag_filter == "exploring" and e["stars"] in (1, 2))]
#     if week_filter:
#         try:
#             week_num = int(week_filter)
#             start_week = datetime.now() - timedelta(weeks=week_num - 1, days=datetime.now().weekday())
#             end_week = start_week + timedelta(days=6)
#             filtered = [e for e in filtered if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]
#         except ValueError:
#             pass
#     if day_filter:
#         try:
#             day_date = datetime.strptime(day_filter, "%Y-%m-%d").date()
#             filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date() == day_date]
#         except ValueError:
#             pass
#     if search_query and not any([tag_filter, week_filter, day_filter]):
#         filtered = [e for e in filtered if search_query.lower() in e["name"].lower()]

#     if not filtered:
#         st.info(get_text("no_entries"))
#         return

#     filtered.sort(key=lambda e: e["date"], reverse=True)
#     current_date = datetime.now()
#     start_week = current_date - timedelta(days=current_date.weekday())
#     end_week = start_week + timedelta(days=6)
#     week_history = [e for e in enriched if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]

#     if week_history:
#         count = len(week_history)
#         most_dish = Counter(e["name"] for e in week_history).most_common(1)[0][0]
#         st.info(get_text("stats_week").format(count=count, dish=most_dish))

#     groups = defaultdict(list)
#     for e in filtered:
#         groups[datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date()].append(e)

#     for day in sorted(groups.keys(), reverse=True):
#         with st.container():
#             st.markdown('<div class="food-card">', unsafe_allow_html=True)
#             st.subheader(day.strftime("%Y-%m-%d"))
#             for e in groups[day]:
#                 col1, col2 = st.columns([5, 1])
#                 with col1:
#                     st.markdown(f"<span class='dish-name'>{html.escape(e['name'])}</span>", unsafe_allow_html=True)
#                 with col2:
#                     st.markdown(f"<span class='stars'>{'⭐' * e['stars']}</span>", unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

# def auth_gate_tabs() -> None:
#     """Hiển thị các tab xác thực cho đăng nhập, đăng ký và đặt lại mật khẩu."""
#     tabs = st.tabs([get_text("login"), get_text("register"), get_text("reset_password")])
#     with tabs[0]:
#         username = st.text_input(get_text("username"), key="login_username")
#         password = st.text_input(get_text("password"), type="password", key="login_password")
#         if st.button(get_text("login_button")):
#             try:
#                 user_id = DatabaseManager.verify_login(username, password)
#                 if user_id:
#                     st.session_state.update(user_id=user_id, username=username)
#                     st.success(get_text("login_button") + " successful!")
#                     st.rerun()
#                 else:
#                     st.error("Invalid username or password.")
#             except Exception as e:
#                 logger.error(f"Lỗi trong quá trình đăng nhập: {e}")
#                 st.error(get_text("db_error").format(error=e))
#     with tabs[1]:
#         username = st.text_input(get_text("username"), key="register_username")
#         password = st.text_input(get_text("password"), type="password", key="register_password")
#         sec_question = st.text_input(get_text("sec_question"), key="sec_question")
#         sec_answer = st.text_input(get_text("sec_answer"), type="password", key="sec_answer")
#         if st.button(get_text("create_account")):
#             try:
#                 success, message = DatabaseManager.create_user(username, password, sec_question, sec_answer)
#                 if success:
#                     st.success(message)
#                     user_id = DatabaseManager.verify_login(username, password)
#                     if user_id:
#                         st.session_state.update(user_id=user_id, username=username)
#                         st.rerun()
#                 else:
#                     st.error(message)
#             except Exception as e:
#                 logger.error(f"Lỗi trong quá trình đăng ký: {e}")
#                 st.error(get_text("db_error").format(error=e))
#     with tabs[2]:
#         username = st.text_input(get_text("username"), key="reset_username")
#         sec_answer = st.text_input(get_text("sec_answer"), type="password", key="reset_sec_answer")
#         new_password = st.text_input(get_text("new_password"), type="password", key="new_password")
#         if st.button(get_text("reset_button")):
#             try:
#                 if DatabaseManager.reset_password(username, sec_answer, new_password):
#                     st.success("Password reset successfully.")
#                 else:
#                     st.error("Invalid username or security answer.")
#             except Exception as e:
#                 logger.error(f"Lỗi trong quá trình đặt lại mật khẩu: {e}")
#                 st.error(get_text("db_error").format(error=e))

# def main() -> None:
#     """Điểm vào ứng dụng chính."""
#     try:
#         initialize_session_state()
#         inject_css()
#         st.title(get_text("app_title"))
#         if current_user_id():
#             topbar_account()
#             tabs = st.tabs([
#                 get_text("inventory"),
#                 get_text("recipes"),
#                 get_text("feasibility"),
#                 get_text("shopping_list"),
#                 get_text("adjust_recipe"),
#                 get_text("food_timeline")
#             ])
#             with tabs[0]:
#                 inventory_page()
#             with tabs[1]:
#                 recipes_page()
#             with tabs[2]:
#                 feasibility_page()
#             with tabs[3]:
#                 shopping_list_page()
#             with tabs[4]:
#                 recipe_adjustment_page()
#             with tabs[5]:
#                 food_timeline_page()
#         else:
#             auth_gate_tabs()
#     except Exception as e:
#         logger.error(f"Lỗi trong hàm chính: {e}")
#         st.error("Đã xảy ra lỗi không mong muốn. Vui lòng làm mới trang hoặc liên hệ hỗ trợ.")

# if __name__ == "__main__":
#     main()








# ### tiếp tục chỉnh sửa Sử dụng bcrypt PostgreSQL

# import streamlit as st
# import html
# from datetime import datetime, timedelta
# from typing import Optional, Dict, List, Tuple, Any
# import logging
# from collections import defaultdict, Counter
# import re
# import bcrypt
# from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.sql import func
# from dotenv import load_dotenv
# import os
# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# # Load environment variables
# load_dotenv()

# # Thiết lập logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# if not logger.handlers:
#     logger.addHandler(handler)

# # Constants
# APP_TITLE_EN = "RuaDen Recipe App"
# APP_TITLE_VI = "Ứng dụng Công thức RuaDen"
# VALID_UNITS = ["g", "kg", "ml", "l", "tsp", "tbsp", "cup", "piece", "pcs", "lạng", "chén", "bát"]

# # Database configuration
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/recipe_app")
# POSTGRES_SUPERUSER = os.getenv("POSTGRES_SUPERUSER", "postgres")
# POSTGRES_SUPERUSER_PASSWORD = os.getenv("POSTGRES_SUPERUSER_PASSWORD", "postgres")
# ROLE_NAME = "recipe_user"
# ROLE_PASSWORD = "secure_password_123"
# DB_NAME = "recipe_app"

# # Văn bản đa ngôn ngữ
# TEXT = {
#     "English": {
#         "app_title": APP_TITLE_EN,
#         "login": "🔐 Login",
#         "username": "Username",
#         "password": "Password",
#         "login_button": "Login",
#         "register": "🆕 Register",
#         "sec_question": "Security Question (for password reset)",
#         "sec_answer": "Security Answer",
#         "create_account": "Create Account",
#         "reset_password": "♻️ Reset Password",
#         "new_password": "New Password",
#         "reset_button": "Reset Password",
#         "logout": "Logout",
#         "language": "Language",
#         "title": "Title",
#         "category": "Category",
#         "instructions": "Instructions",
#         "servings": "Servings",
#         "name": "Name",
#         "quantity": "Quantity",
#         "unit": "Unit",
#         "need": "Need",
#         "have": "Have",
#         "missing": "Missing",
#         "inventory": "📦 Inventory",
#         "your_stock": "Your Stock",
#         "no_ingredients": "No ingredients yet.",
#         "unit_tips": "Unit tips: use g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
#         "add_ingredient": "Add New Ingredient",
#         "recipes": "📖 Recipes",
#         "your_recipes": "Your Recipes",
#         "no_recipes": "No recipes yet.",
#         "save_recipe": "Save Recipe",
#         "update_recipe": "Update Recipe",
#         "delete_recipe": "Delete Recipe",
#         "feasibility": "✅ Feasibility & Shopping",
#         "create_recipes_first": "Create recipes first.",
#         "you_can_cook": "Recipe Feasibility and Shopping List",
#         "none_yet": "None yet.",
#         "all_available": "All ingredients available.",
#         "cook": "Cook",
#         "missing_something": "Missing Ingredients",
#         "all_feasible": "All recipes are feasible 🎉",
#         "add_to_shopping": "Add missing to Shopping List",
#         "shopping_list": "🛒 Shopping List",
#         "empty_list": "Your shopping list is empty.",
#         "update_inventory": "Update Inventory from Shopping List",
#         "purchased": "Inventory updated with purchased items.",
#         "select_recipes_label": "Select recipes to proceed",
#         "select_purchased": "Select purchased items",
#         "sent_to_shopping": "Missing ingredients added to the shopping list.",
#         "cook_success": "Cooked successfully.",
#         "cook_failed": "Cooking failed: {error}",
#         "adjust_recipe": "⚖️ Adjust Recipe",
#         "select_recipe": "Select Recipe",
#         "adjustment_type": "Adjustment Type",
#         "by_servings": "By Servings",
#         "by_main_ingredient": "By Main Ingredient",
#         "new_servings": "New Servings",
#         "main_ingredient": "Main Ingredient",
#         "new_quantity": "New Quantity",
#         "spice_level": "Spice Adjustment",
#         "mild": "Mild (60%)",
#         "normal": "Normal (80%)",
#         "rich": "Rich (100%)",
#         "adjusted_recipe": "Adjusted Recipe",
#         "cook_adjusted": "Cook Adjusted Recipe",
#         "add_to_shopping_adjusted": "Add Missing to Shopping List",
#         "adjusted_recipe_title": "Adjusted: {title}",
#         "no_recipe_selected": "Please select a recipe to adjust.",
#         "invalid_adjustment": "Invalid adjustment parameters.",
#         "cook_adjusted_success": "Adjusted recipe '{title}' cooked successfully.",
#         "cook_adjusted_failed": "Failed to cook adjusted recipe '{title}': {error}",
#         "not_logged_in": "You must be logged in to access this page.",
#         "error_title_required": "Recipe title is required.",
#         "error_ingredients_required": "At least one valid ingredient (with name and positive quantity) is required.",
#         "duplicate_recipe": "A recipe with this title already exists.",
#         "error_invalid_name": "Invalid ingredient name: {name}",
#         "error_invalid_unit": "Invalid unit: {unit}",
#         "error_negative_qty": "Quantity must be positive for ingredient: {name}",
#         "save_success": "Recipe '{title}' saved successfully.",
#         "update_success": "Recipe '{title}' updated successfully.",
#         "delete_success": "Recipe '{title}' deleted successfully.",
#         "save_failed": "Failed to save recipe '{title}': {error}",
#         "update_failed": "Failed to update recipe '{title}': {error}",
#         "delete_failed": "Failed to delete recipe '{title}'.",
#         "food_timeline": "🍲 Food Timeline",
#         "no_history": "No cooking history yet.",
#         "no_entries": "No entries match the filters.",
#         "congrats": "Congratulations! You have reached {stars} with {dish} 🎉",
#         "signature_dish": "Signature Dish",
#         "search_placeholder": "Search (e.g., tag:signature, week:1, day:2025-09-01)",
#         "reset_filter": "🔄 Reset filter",
#         "stats_week": "This week you cooked {count} dishes, most frequent: {dish}",
#         "db_error": "Database error: {error}",
#         "save_changes": "Save Changes",
#         "inventory_updated": "Inventory updated successfully.",
#         "db_init_failed": "Failed to initialize database: {error}"
#     },
#     "Vietnamese": {
#         # Same as original, omitted for brevity
#     }
# }

# # Database initialization
# def initialize_database() -> bool:
#     """Initialize PostgreSQL database and role if they don't exist."""
#     try:
#         # Connect as superuser to create role and database
#         conn = psycopg2.connect(
#             dbname="postgres",
#             user=POSTGRES_SUPERUSER,
#             password=POSTGRES_SUPERUSER_PASSWORD,
#             host="localhost",
#             port=5432
#         )
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         cursor = conn.cursor()

#         # Check if role exists
#         cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (ROLE_NAME,))
#         if not cursor.fetchone():
#             cursor.execute(f"CREATE ROLE {ROLE_NAME} WITH LOGIN PASSWORD %s", (ROLE_PASSWORD,))
#             logger.info(f"Created PostgreSQL role: {ROLE_NAME}")

#         # Check if database exists
#         cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
#         if not cursor.fetchone():
#             cursor.execute(f"CREATE DATABASE {DB_NAME}")
#             cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {ROLE_NAME}")
#             logger.info(f"Created PostgreSQL database: {DB_NAME}")

#         cursor.close()
#         conn.close()
#         return True
#     except Exception as e:
#         logger.error(f"Failed to initialize database: {e}")
#         return False

# # Database setup
# try:
#     if not initialize_database():
#         st.error(get_text("db_init_failed").format(error="Could not initialize database. Check logs for details."))
#         st.stop()
#     engine = create_engine(DATABASE_URL, echo=False)
#     Base = declarative_base()
#     Session = sessionmaker(bind=engine)
# except Exception as e:
#     logger.error(f"Failed to connect to database: {e}")
#     st.error(get_text("db_error").format(error=str(e)))
#     st.stop()

# # Database Models
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     username = Column(String(255), unique=True, nullable=False)
#     password_hash = Column(String(128), nullable=False)
#     sec_question = Column(String(255), nullable=False)
#     sec_answer_hash = Column(String(128), nullable=False)
#     inventory = relationship("Inventory", back_populates="user")
#     recipes = relationship("Recipe", back_populates="user")
#     cooked_history = relationship("CookedHistory", back_populates="user")

# class Inventory(Base):
#     __tablename__ = "inventory"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     name = Column(String(255), nullable=False)
#     quantity = Column(Float, nullable=False)
#     unit = Column(String(50), nullable=False)
#     user = relationship("User", back_populates="inventory")

# class Recipe(Base):
#     __tablename__ = "recipes"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     title = Column(String(255), nullable=False)
#     category = Column(String(255))
#     instructions = Column(Text)
#     servings = Column(Float, default=1.0)
#     is_signature = Column(Boolean, default=False)
#     user = relationship("User", back_populates="recipes")
#     ingredients = relationship("RecipeIngredient", back_populates="recipe")

# class RecipeIngredient(Base):
#     __tablename__ = "recipe_ingredients"
#     id = Column(Integer, primary_key=True)
#     recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
#     name = Column(String(255), nullable=False)
#     quantity = Column(Float, nullable=False)
#     unit = Column(String(50), nullable=False)
#     is_spice = Column(Boolean, default=False)
#     recipe = relationship("Recipe", back_populates="ingredients")

# class CookedHistory(Base):
#     __tablename__ = "cooked_history"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
#     cooked_date = Column(DateTime, default=func.now())
#     user = relationship("User", back_populates="cooked_history")

# # Create tables
# try:
#     Base.metadata.create_all(engine)
# except Exception as e:
#     logger.error(f"Failed to create tables: {e}")
#     st.error(get_text("db_error").format(error=str(e)))
#     st.stop()

# # Danh sách export
# __all__ = [
#     'inject_css', 'get_text', 'current_user_id', 'initialize_session_state',
#     'topbar_account', 'inventory_page', 'recipes_page', 'feasibility_page',
#     'shopping_list_page', 'recipe_adjustment_page', 'food_timeline_page',
#     'auth_gate_tabs', 'main'
# ]

# def inject_css() -> None:
#     """Tiêm CSS tùy chỉnh để định dạng ứng dụng Streamlit."""
#     try:
#         st.markdown(
#             """
#             <style>
#                 .block-container {
#                     padding-top: 5rem;
#                     padding-bottom: 2rem;
#                     max-width: 980px;
#                 }
#                 .stTextInput > div > div > input,
#                 .stNumberInput > div > div > input,
#                 textarea {
#                     border-radius: 12px !important;
#                     border: 1px solid #e6e6e6 !important;
#                     padding: .55rem .8rem !important;
#                 }
#                 .stButton > button {
#                     background: #111 !important;
#                     color: #fff !important;
#                     border: none !important;
#                     border-radius: 14px !important;
#                     padding: .55rem 1rem !important;
#                     font-weight: 500 !important;
#                     transition: transform .12s ease, opacity .12s ease;
#                 }
#                 .stButton > button:hover {
#                     transform: translateY(-1px);
#                     opacity: .95;
#                 }
#                 table {
#                     border-collapse: collapse;
#                     width: 100%;
#                 }
#                 th, td {
#                     padding: 8px 10px;
#                     border-bottom: 1px solid #eee;
#                 }
#                 th {
#                     color: #666;
#                     font-weight: 600;
#                 }
#                 td {
#                     color: #222;
#                 }
#                 .stTabs [data-baseweb="tab-list"] {
#                     gap: .25rem;
#                     margin-top: 1rem;
#                 }
#                 .stTabs [data-baseweb="tab"] {
#                     padding: .6rem 1rem;
#                 }
#                 .streamlit-expanderHeader {
#                     font-weight: 600;
#                 }
#                 #topbar-account {
#                     margin-bottom: 1rem;
#                 }
#                 .food-card {
#                     border: 1px solid #eee;
#                     border-radius: 12px;
#                     padding: 1rem;
#                     margin-bottom: 1rem;
#                     background-color: #f9f9f9;
#                 }
#                 .dish-name {
#                     font-weight: bold;
#                     font-size: 1.2em;
#                 }
#                 .stars {
#                     font-size: 1.2em;
#                     color: #FFD700;
#                     text-align: right;
#                 }
#                 @media (max-width: 600px) {
#                     .block-container {
#                         padding-top: 4rem;
#                         padding-left: 1rem;
#                         padding-right: 1rem;
#                     }
#                     .stButton > button {
#                         width: 100%;
#                         margin-bottom: 0.5rem;
#                     }
#                     .stTabs [data-baseweb="tab-list"] {
#                         margin-top: 0.5rem;
#                     }
#                 }
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )
#     except Exception as e:
#         logger.error(f"Lỗi tiêm CSS: {e}")
#         st.error("Không thể áp dụng kiểu dáng tùy chỉnh. Tiếp tục với kiểu mặc định.")

# def get_text(key: str, **kwargs) -> str:
#     """Truy xuất văn bản đa ngôn ngữ với format an toàn."""
#     lang = st.session_state.get("language", "English")
#     template = TEXT.get(lang, TEXT["English"]).get(key, key)
#     if kwargs:
#         try:
#             return template.format(**kwargs)
#         except Exception as e:
#             logger.warning(f"i18n fallback cho key='{key}': {e}")
#             return template
#     return template

# def current_user_id() -> Optional[int]:
#     """Lấy ID người dùng hiện tại từ session_state."""
#     return st.session_state.get("user_id")

# def initialize_session_state() -> None:
#     """Khởi tạo trạng thái phiên với các giá trị mặc định."""
#     defaults = {
#         "user_id": None,
#         "username": None,
#         "language": "English",
#         "editing_recipe_id": None,
#         "recipe_form_data": {
#             "title": "",
#             "category": "",
#             "instructions": "",
#             "is_signature": False,
#             "servings": 1.0,
#             "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#         },
#         "shopping_list_data": [],
#         "adjusted_recipe": None,
#         "search_value": ""
#     }
#     for key, value in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = value

# def topbar_account() -> None:
#     """Hiển thị thanh trên cùng với tên người dùng, chọn ngôn ngữ và nút đăng xuất."""
#     user_id = current_user_id()
#     if not user_id:
#         return
#     with st.container():
#         st.markdown('<div id="topbar-account">', unsafe_allow_html=True)
#         col1, col2, col3 = st.columns([3, 1, 1])
#         with col1:
#             st.write(f"{get_text('username')}: {html.escape(st.session_state.get('username', 'Unknown'))}")
#         with col2:
#             st.selectbox(
#                 get_text("language"),
#                 ["English", "Vietnamese"],
#                 index=0 if st.session_state.get("language", "English") == "English" else 1,
#                 key="language_selector",
#                 on_change=lambda: st.session_state.update({"language": st.session_state.language_selector})
#             )
#         with col3:
#             if st.button(get_text("logout")):
#                 st.session_state.clear()
#                 initialize_session_state()
#                 logger.info(f"User {st.session_state.get('username', 'Unknown')} logged out")
#                 st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)

# def calculate_stars(count: int, is_signature: bool) -> int:
#     """Tính số sao dựa trên số lần nấu và trạng thái món tủ."""
#     if not isinstance(count, int) or count < 0:
#         return 0
#     thresholds = [(15, 5), (8, 4), (5, 3), (3, 2), (1, 1)]
#     return 5 if is_signature else next((stars for threshold, stars in thresholds if count >= threshold), 0)

# # Helper functions
# def _norm_name(name: str) -> str:
#     """Chuẩn hóa tên nguyên liệu để so sánh."""
#     return (name or "").strip().lower()

# def _norm_unit(unit: str) -> str:
#     """Chuẩn hóa đơn vị để so sánh."""
#     return (unit or "").strip().lower()

# def _inventory_map(user_id: int) -> Dict[Tuple[str, str], dict]:
#     """Tạo bản đồ kho dựa trên tên và đơn vị chuẩn hóa."""
#     session = Session()
#     try:
#         items = session.query(Inventory).filter_by(user_id=user_id).all()
#         return {
#             (_norm_name(item.name), _norm_unit(item.unit)): {
#                 "id": item.id,
#                 "name": item.name,
#                 "quantity": item.quantity,
#                 "unit": item.unit
#             }
#             for item in items if item.name and item.unit
#         }
#     except SQLAlchemyError as e:
#         logger.error(f"Error fetching inventory map for user {user_id}: {e}")
#         raise
#     finally:
#         session.close()

# def validate_ingredients(recipe: Dict, inventory_map: Dict[Tuple[str, str], dict]) -> Tuple[bool, Optional[str]]:
#     """Kiểm tra tính hợp lệ và khả thi của các nguyên liệu trong công thức."""
#     if not recipe.get("ingredients"):
#         return False, get_text("error_ingredients_required")
    
#     for ing in recipe.get("ingredients", []):
#         name = _norm_name(ing.get("name", ""))
#         unit = _norm_unit(ing.get("unit", ""))
#         qty = float(ing.get("quantity", 0.0))
        
#         if not name or qty <= 0:
#             return False, get_text("error_ingredients_required")
#         if not DatabaseManager.validate_name(ing.get("name", "")):
#             return False, get_text("error_invalid_name").format(name=ing.get("name"))
#         if unit not in [_norm_unit(u) for u in VALID_UNITS]:
#             return False, get_text("error_invalid_unit").format(unit=ing.get("unit"))
        
#         key = (name, unit)
#         inv_item = inventory_map.get(key)
#         if not inv_item:
#             return False, f"Ingredient {ing.get('name')} not found in inventory"
#         if inv_item["unit"] != ing.get("unit"):
#             return False, f"Unit mismatch for {ing.get('name')}: expected {ing.get('unit')}, found {inv_item['unit']}"
#         if inv_item["quantity"] < qty:
#             return False, f"Insufficient quantity for {ing.get('name')}: need {qty}, have {inv_item['quantity']}"
    
#     return True, None

# def recipe_feasibility(recipe: Dict, user_id: int) -> Tuple[bool, List[Dict]]:
#     """Kiểm tra tính khả thi của công thức dựa trên kho."""
#     try:
#         inv_map = _inventory_map(user_id)
#         shorts = []
#         feasible = True
        
#         for ing in recipe.get("ingredients", []):
#             name = _norm_name(ing.get("name", ""))
#             unit = _norm_unit(ing.get("unit", ""))
#             qty = float(ing.get("quantity", 0.0))
#             key = (name, unit)
#             inv_item = inv_map.get(key, {})
#             have_qty = float(inv_item.get("quantity", 0.0))
#             missing = max(0.0, qty - have_qty)
            
#             if missing > 1e-9 or not inv_item:
#                 feasible = False
#                 shorts.append({
#                     "name": ing.get("name", ""),
#                     "needed_qty": qty,
#                     "have_qty": have_qty,
#                     "needed_unit": ing.get("unit", ""),
#                     "have_unit": inv_item.get("unit", "") if inv_item else "",
#                     "missing_qty_disp": missing,
#                     "missing_unit_disp": ing.get("unit", "")
#                 })
        
#         return feasible, shorts
#     except SQLAlchemyError as e:
#         logger.error(f"Error checking recipe feasibility: {e}")
#         raise

# def consume_ingredients_for_recipe(recipe: Dict, user_id: int) -> Tuple[bool, str]:
#     """Tiêu thụ nguyên liệu từ kho nếu công thức khả thi."""
#     session = Session()
#     try:
#         inv_map = _inventory_map(user_id)
#         is_valid, error = validate_ingredients(recipe, inv_map)
#         if not is_valid:
#             logger.warning(f"Validation failed for recipe {recipe.get('title', 'Unknown')}: {error}")
#             return False, get_text("cook_failed").format(error=error)
        
#         for ing in recipe.get("ingredients", []):
#             name = _norm_name(ing.get("name", ""))
#             unit = _norm_unit(ing.get("unit", ""))
#             qty = float(ing.get("quantity", 0.0))
#             key = (name, unit)
#             inv_item = inv_map.get(key)
            
#             if not inv_item:
#                 raise ValueError(f"Ingredient {ing.get('name')} not found in inventory")
#             if inv_item["unit"] != ing.get("unit"):
#                 raise ValueError(f"Unit mismatch for {ing.get('name')}")
#             if inv_item["quantity"] < qty:
#                 raise ValueError(f"Insufficient quantity for {ing.get('name')}")
            
#             inventory_item = session.query(Inventory).filter_by(id=inv_item["id"]).first()
#             inventory_item.quantity = max(0.0, inventory_item.quantity - qty)
        
#         session.commit()
#         logger.info(f"Successfully consumed ingredients for recipe {recipe.get('title', 'Unknown')}")
#         return True, get_text("cook_success")
#     except Exception as e:
#         session.rollback()
#         logger.error(f"Failed to consume ingredients for recipe {recipe.get('title', 'Unknown')}: {str(e)}")
#         return False, get_text("cook_failed").format(error=str(e))
#     finally:
#         session.close()

# class DatabaseManager:
#     @staticmethod
#     def validate_name(name: str) -> bool:
#         """Kiểm tra tên nguyên liệu hợp lệ."""
#         return bool(name.strip() and re.match(r'^[\w\s\-\']+$', name))

#     @staticmethod
#     def normalize_name(name: str) -> str:
#         """Chuẩn hóa tên để so sánh."""
#         return _norm_name(name)

#     @classmethod
#     def verify_login(cls, username: str, password: str) -> Optional[int]:
#         """Xác minh đăng nhập."""
#         if not username or not password or len(password) < 8:
#             return None
#         session = Session()
#         try:
#             user = session.query(User).filter_by(username=username).first()
#             if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
#                 return user.id
#             return None
#         except SQLAlchemyError as e:
#             logger.error(f"Error verifying login for {username}: {e}")
#             raise
#         finally:
#             session.close()

#     @classmethod
#     def create_user(cls, username: str, password: str, sec_question: str, sec_answer: str) -> Tuple[bool, str]:
#         """Tạo người dùng mới."""
#         if not all([username.strip(), password.strip(), sec_question.strip(), sec_answer.strip()]):
#             return False, "All fields required."
#         if len(password) < 8:
#             return False, "Password must be at least 8 characters."
#         if not cls.validate_name(username):
#             return False, get_text("error_invalid_name").format(name=username)
        
#         session = Session()
#         try:
#             if session.query(User).filter_by(username=username).first():
#                 return False, "Username already exists."
#             password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#             sec_answer_hash = bcrypt.hashpw(sec_answer.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#             user = User(
#                 username=username,
#                 password_hash=password_hash,
#                 sec_question=sec_question,
#                 sec_answer_hash=sec_answer_hash
#             )
#             session.add(user)
#             session.commit()
#             logger.info(f"Created user: {username}")
#             return True, "User created successfully."
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Error creating user {username}: {e}")
#             return False, get_text("db_error").format(error=str(e))
#         finally:
#             session.close()

#     @classmethod
#     def reset_password(cls, username: str, sec_answer: str, new_password: str) -> bool:
#         """Đặt lại mật khẩu."""
#         if not all([username.strip(), sec_answer.strip(), new_password.strip()]):
#             return False
#         if len(new_password) < 8:
#             return False
#         session = Session()
#         try:
#             user = session.query(User).filter_by(username=username).first()
#             if not user:
#                 return False
#             if bcrypt.checkpw(sec_answer.encode('utf-8'), user.sec_answer_hash.encode('utf-8')):
#                 user.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 session.commit()
#                 logger.info(f"Password reset for user: {username}")
#                 return True
#             return False
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Error resetting password for {username}: {e}")
#             return False
#         finally:
#             session.close()

#     @classmethod
#     def list_inventory(cls, user_id: int) -> List[Dict]:
#         """Liệt kê kho của người dùng."""
#         session = Session()
#         try:
#             items = session.query(Inventory).filter_by(user_id=user_id).all()
#             return [
#                 {"id": item.id, "name": item.name, "quantity": item.quantity, "unit": item.unit}
#                 for item in items
#             ]
#         except SQLAlchemyError as e:
#             logger.error(f"Error listing inventory for user {user_id}: {e}")
#             raise
#         finally:
#             session.close()

#     @classmethod
#     def upsert_inventory(cls, user_id: int, name: str, quantity: float, unit: str) -> None:
#         """Thêm hoặc cập nhật item trong kho."""
#         session = Session()
#         try:
#             item = session.query(Inventory).filter_by(
#                 user_id=user_id,
#                 name=cls.normalize_name(name),
#                 unit=_norm_unit(unit)
#             ).first()
#             if item:
#                 item.quantity = max(0.0, item.quantity + quantity)
#             else:
#                 item = Inventory(
#                     user_id=user_id,
#                     name=name,
#                     quantity=max(0.0, quantity),
#                     unit=unit
#                 )
#                 session.add(item)
#             session.commit()
#             logger.info(f"Upserted inventory item: {name} for user {user_id}")
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Error upserting inventory for user {user_id}: {e}")
#             raise
#         finally:
#             session.close()

#     @classmethod
#     def update_inventory_item(cls, user_id: int, item_id: int, name: str, quantity: float, unit: str) -> bool:
#         """Cập nhật item cụ thể trong kho theo ID."""
#         session = Session()
#         try:
#             item = session.query(Inventory).filter_by(id=item_id, user_id=user_id).first()
#             if not item:
#                 logger.error(f"Inventory item not found: id={item_id}, user_id={user_id}")
#                 return False
#             if not cls.validate_name(name):
#                 logger.error(f"Invalid name for inventory item: {name}")
#                 return False
#             if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                 logger.error(f"Invalid unit for inventory item: {unit}")
#                 return False
#             if quantity < 0:
#                 logger.error(f"Negative quantity for inventory item: {name}")
#                 return False
#             item.name = name
#             item.quantity = max(0.0, quantity)
#             item.unit = unit
#             session.commit()
#             logger.info(f"Updated inventory item: id={item_id} for user {user_id}")
#             return True
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Error updating inventory item {item_id}: {e}")
#             return False
#         finally:
#             session.close()

#     @classmethod
#     def delete_inventory(cls, user_id: int, item_id: int) -> None:
#         """Xóa item khỏi kho theo ID."""
#         session = Session()
#         try:
#             item = session.query(Inventory).filter_by(id=item_id, user_id=user_id).first()
#             if item:
#                 session.delete(item)
#                 session.commit()
#                 logger.info(f"Deleted inventory item: id={item_id} for user {user_id}")
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Error deleting inventory item {item_id}: {e}")
#             raise
#         finally:
#             session.close()

#     @classmethod
#     def list_recipes(cls, user_id: int) -> List[Dict]:
#         """Liệt kê công thức của người dùng."""
#         session = Session()
#         try:
#             recipes = session.query(Recipe).filter_by(user_id=user_id).all()
#             return [
#                 {
#                     "id": r.id,
#                     "title": r.title,
#                     "category": r.category,
#                     "instructions": r.instructions,
#                     "servings": r.servings,
#                     "is_signature": r.is_signature,
#                     "ingredients": [
#                         {
#                             "name": i.name,
#                             "quantity": i.quantity,
#                             "unit": i.unit,
#                             "is_spice": i.is_spice
#                         } for i in r.ingredients
#                     ]
#                 } for r in recipes
#             ]
#         except SQLAlchemyError as e:
#             logger.error(f"Error listing recipes for user {user_id}: {e}")
#             raise
#         finally:
#             session.close()

#     @classmethod
#     def create_recipe(cls, user_id: int, title: str, category: str, instructions: str, 
#                       ingredients: List[Dict], recipe_id: Optional[int] = None, is_signature: bool = False) -> Tuple[bool, str]:
#         """Tạo hoặc cập nhật công thức."""
#         session = Session()
#         try:
#             if not title.strip():
#                 return False, get_text("error_title_required")
#             if not any(ing["name"].strip() and ing["quantity"] > 0 for ing in ingredients):
#                 return False, get_text("error_ingredients_required")
            
#             if session.query(Recipe).filter_by(user_id=user_id, title=title).filter(Recipe.id != recipe_id).first():
#                 return False, get_text("duplicate_recipe")
            
#             if recipe_id:
#                 recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
#                 if not recipe:
#                     return False, get_text("delete_failed").format(title=title)
#                 recipe.title = title
#                 recipe.category = category
#                 recipe.instructions = instructions
#                 recipe.is_signature = is_signature
#                 recipe.servings = 1.0
#                 session.query(RecipeIngredient).filter_by(recipe_id=recipe_id).delete()
#             else:
#                 recipe = Recipe(
#                     user_id=user_id,
#                     title=title,
#                     category=category,
#                     instructions=instructions,
#                     servings=1.0,
#                     is_signature=is_signature
#                 )
#                 session.add(recipe)
#                 session.flush()  # Get recipe.id before committing
            
#             for ing in ingredients:
#                 session.add(RecipeIngredient(
#                     recipe_id=recipe.id,
#                     name=ing["name"],
#                     quantity=ing["quantity"],
#                     unit=ing["unit"],
#                     is_spice=ing.get("is_spice", False)
#                 ))
            
#             session.commit()
#             logger.info(f"{'Updated' if recipe_id else 'Created'} recipe: {title} for user {user_id}")
#             return True, get_text("update_success" if recipe_id else "save_success").format(title=title)
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Error saving recipe {title}: {e}")
#             return False, get_text("save_failed").format(title=title, error=str(e))
#         finally:
#             session.close()

#     @classmethod
#     def delete_recipe(cls, user_id: int, recipe_id: int) -> bool:
#         """Xóa công thức."""
#         session = Session()
#         try:
#             recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
#             if recipe:
#                 session.delete(recipe)
#                 session.commit()
#                 logger.info(f"Deleted recipe: id={recipe_id} for user {user_id}")
#                 return True
#             return False
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Error deleting recipe {recipe_id}: {e}")
#             return False
#         finally:
#             session.close()

#     @classmethod
#     def log_cooked_recipe(cls, user_id: int, recipe_id: int) -> None:
#         """Ghi log công thức đã nấu."""
#         session = Session()
#         try:
#             session.add(CookedHistory(user_id=user_id, recipe_id=recipe_id))
#             session.commit()
#             logger.info(f"Logged cooked recipe: id={recipe_id} for user {user_id}")
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Error logging cooked recipe {recipe_id}: {e}")
#             raise
#         finally:
#             session.close()

#     @classmethod
#     def list_cooked_history(cls, user_id: int) -> List[Dict]:
#         """Liệt kê lịch sử nấu ăn."""
#         session = Session()
#         try:
#             history = session.query(CookedHistory).filter_by(user_id=user_id).all()
#             return [
#                 {"recipe_id": h.recipe_id, "cooked_date": h.cooked_date.strftime("%Y-%m-%d %H:%M:%S")}
#                 for h in history
#             ]
#         except SQLAlchemyError as e:
#             logger.error(f"Error listing cooked history for user {user_id}: {e}")
#             raise
#         finally:
#             session.close()

#     @classmethod
#     def get_cooked_count(cls, user_id: int, recipe_id: int) -> int:
#         """Lấy số lần nấu công thức."""
#         session = Session()
#         try:
#             return session.query(CookedHistory).filter_by(user_id=user_id, recipe_id=recipe_id).count()
#         except SQLAlchemyError as e:
#             logger.error(f"Error getting cooked count for recipe {recipe_id}: {e}")
#             raise
#         finally:
#             session.close()

# def inventory_page() -> None:
#     """Hiển thị và quản lý kho nguyên liệu."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Lỗi tải kho cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     st.header(get_text("inventory"))
#     st.subheader(get_text("your_stock"))
#     st.caption(get_text("unit_tips"))

#     with st.expander(get_text("add_ingredient")):
#         with st.form(key="add_inventory_form"):
#             col1, col2, col3 = st.columns([2, 1, 1])
#             with col1:
#                 ingredient_name = st.text_input(get_text("name"), placeholder=get_text("e.g., chicken"), key="new_ingredient_name")
#             with col2:
#                 quantity = st.number_input(get_text("quantity"), min_value=0.0, step=0.1, value=0.0, key="new_quantity")
#             with col3:
#                 unit = st.selectbox(get_text("unit"), options=VALID_UNITS, key="new_unit")
#             if st.form_submit_button(get_text("add_ingredient")):
#                 if not ingredient_name.strip() or quantity < 0:
#                     st.error(get_text("error_ingredients_required"))
#                 elif not DatabaseManager.validate_name(ingredient_name):
#                     st.error(get_text("error_invalid_name").format(name=ingredient_name))
#                 elif not _norm_unit(unit) in [_norm_unit(u) for u in VALID_UNITS]:
#                     st.error(get_text("error_invalid_unit").format(unit=unit))
#                 else:
#                     try:
#                         DatabaseManager.upsert_inventory(user_id, ingredient_name.strip(), quantity, unit)
#                         st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                         st.success(get_text("save_success").format(title=ingredient_name))
#                         st.rerun()
#                     except SQLAlchemyError as e:
#                         logger.error(f"Lỗi thêm nguyên liệu {ingredient_name}: {e}")
#                         st.error(get_text("db_error").format(error=e))

#     edited_data = st.data_editor(
#         inventory,
#         column_config={
#             "id": None,
#             "name": st.column_config.TextColumn(get_text("name"), required=True),
#             "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
#             "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#         },
#         num_rows="dynamic",
#         key=f"inventory_editor_{user_id}",
#         hide_index=True
#     )

#     if st.button(get_text("save_changes")):
#         errors = []
#         for item in edited_data:
#             name = item.get("name", "").strip()
#             quantity = item.get("quantity")
#             unit = item.get("unit", "")
#             if not name or not isinstance(quantity, (int, float)) or quantity < 0 or not unit:
#                 errors.append(get_text("error_ingredients_required"))
#                 continue
#             if not DatabaseManager.validate_name(name):
#                 errors.append(get_text("error_invalid_name").format(name=name))
#                 continue
#             if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                 errors.append(get_text("error_invalid_unit").format(unit=unit))
#                 continue
#         if errors:
#             for error in errors:
#                 st.error(error)
#         else:
#             session = Session()
#             try:
#                 old_ids = {item.get("id") for item in inventory if "id" in item}
#                 edited_ids = {item.get("id") for item in edited_data if "id" in item}
#                 deleted_ids = old_ids - edited_ids
#                 for item_id in deleted_ids:
#                     DatabaseManager.delete_inventory(user_id, item_id)
#                 for item in edited_data:
#                     if "id" in item:
#                         if not DatabaseManager.update_inventory_item(user_id, item["id"], item["name"], item["quantity"], item["unit"]):
#                             raise ValueError(f"Failed to update inventory item {item['name']}")
#                     else:
#                         DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"])
#                 session.commit()
#                 st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                 st.success(get_text("inventory_updated"))
#                 st.rerun()
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Lỗi cập nhật kho: {e}")
#                 st.error(get_text("db_error").format(error=e))
#             finally:
#                 session.close()

#     if not inventory:
#         st.info(get_text("no_ingredients"))

# def recipes_page() -> None:
#     """Hiển thị và quản lý công thức của người dùng."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Lỗi tải công thức cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     st.header(get_text("recipes"))
#     st.subheader(get_text("your_recipes"))
#     st.caption(get_text("unit_tips"))

#     if not recipes:
#         st.info(get_text("no_recipes"))

#     form_data = st.session_state.recipe_form_data
#     recipe_id = st.session_state.get("editing_recipe_id")

#     with st.form(key="recipe_form"):
#         title = st.text_input(get_text("title"), value=form_data["title"], key="recipe_title")
#         category = st.text_input(get_text("category"), value=form_data["category"], key="recipe_category")
#         instructions = st.text_area(get_text("instructions"), value=form_data["instructions"], key="recipe_instructions")
#         is_signature = st.checkbox(get_text("signature_dish"), value=form_data["is_signature"], key="recipe_is_signature")
#         ingredients_data = st.data_editor(
#             form_data["ingredients"],
#             column_config={
#                 "name": st.column_config.TextColumn(get_text("name"), required=True),
#                 "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
#                 "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#                 "is_spice": st.column_config.CheckboxColumn("Spice", default=False)
#             },
#             num_rows="dynamic",
#             key="ingredients_editor",
#             hide_index=True
#         )

#         submit_label = get_text("update_recipe") if recipe_id else get_text("save_recipe")
#         if st.form_submit_button(submit_label):
#             if not title.strip():
#                 st.error(get_text("error_title_required"))
#                 return
#             valid_ingredients = [
#                 ing for ing in ingredients_data
#                 if DatabaseManager.normalize_name(ing.get("name", "")).strip() and
#                 isinstance(ing.get("quantity"), (int, float)) and ing["quantity"] > 0 and
#                 _norm_unit(ing.get("unit", "")) in [_norm_unit(u) for u in VALID_UNITS]
#             ]
#             if not valid_ingredients:
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             existing_recipe = next((r for r in recipes if r.get("title") == title.strip() and r.get("id") != recipe_id), None)
#             if existing_recipe:
#                 st.error(get_text("duplicate_recipe"))
#                 return
#             for ing in valid_ingredients:
#                 if not DatabaseManager.validate_name(ing["name"]):
#                     st.error(get_text("error_invalid_name").format(name=ing["name"]))
#                     return
#                 if not _norm_unit(ing["unit"]) in [_norm_unit(u) for u in VALID_UNITS]:
#                     st.error(get_text("error_invalid_unit").format(unit=ing["unit"]))
#                     return
#                 if ing["quantity"] <= 0:
#                     st.error(get_text("error_negative_qty").format(name=ing["name"]))
#                     return
#             try:
#                 success, message = DatabaseManager.create_recipe(
#                     user_id, title.strip(), category.strip(), instructions.strip(), 
#                     valid_ingredients, recipe_id, is_signature
#                 )
#                 if success:
#                     st.success(message)
#                     st.session_state.recipe_form_data = {
#                         "title": "",
#                         "category": "",
#                         "instructions": "",
#                         "is_signature": False,
#                         "servings": 1.0,
#                         "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#                     }
#                     st.session_state.editing_recipe_id = None
#                     st.rerun()
#                 else:
#                     st.error(message)
#             except SQLAlchemyError as e:
#                 logger.error(f"Lỗi lưu công thức {title}: {e}")
#                 st.error(get_text("save_failed").format(title=title, error=str(e)))

#     if recipes:
#         for recipe in recipes:
#             signature_text = f" - {get_text('signature_dish')}" if recipe.get("is_signature") else ""
#             with st.expander(f"{html.escape(recipe.get('title', 'Untitled'))} ({html.escape(recipe.get('category', '-'))}) {signature_text}"):
#                 st.write(f"**{get_text('instructions')}:** {html.escape(recipe.get('instructions', ''))}")
#                 st.table([
#                     {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
#                      get_text("unit"): ing["unit"], "Spice": "Yes" if ing.get("is_spice") else "No"}
#                     for ing in recipe.get("ingredients", [])
#                 ])
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button(get_text("update_recipe"), key=f"edit_{recipe.get('id')}"):
#                         st.session_state.editing_recipe_id = recipe["id"]
#                         st.session_state.recipe_form_data = {
#                             "title": recipe["title"],
#                             "category": recipe["category"],
#                             "instructions": recipe["instructions"],
#                             "is_signature": recipe.get("is_signature", False),
#                             "servings": recipe.get("servings", 1.0),
#                             "ingredients": [
#                                 {"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": ing.get("is_spice", False)}
#                                 for ing in recipe.get("ingredients", [])
#                             ]
#                         }
#                         st.rerun()
#                 with col2:
#                     if st.button(get_text("delete_recipe"), key=f"delete_{recipe.get('id')}"):
#                         try:
#                             if DatabaseManager.delete_recipe(user_id, recipe["id"]):
#                                 st.success(get_text("delete_success").format(title=recipe["title"]))
#                                 st.rerun()
#                             else:
#                                 st.error(get_text("delete_failed").format(title=recipe["title"]))
#                         except SQLAlchemyError as e:
#                             logger.error(f"Lỗi xóa công thức {recipe['title']}: {e}")
#                             st.error(get_text("delete_failed").format(title=recipe["title"]))

# def feasibility_page() -> None:
#     """Hiển thị tính khả thi của công thức và tùy chọn danh sách mua sắm."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Lỗi tải dữ liệu cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     if not recipes:
#         st.info(get_text("create_recipes_first"))
#         return

#     st.header(get_text("feasibility"))
#     st.subheader(get_text("you_can_cook"))

#     recipe_results = [
#         {"recipe": r, "feasible": feasible, "shorts": shorts}
#         for r in recipes
#         for feasible, shorts in [recipe_feasibility(r, user_id)]
#     ]

#     if not recipe_results:
#         st.info(get_text("none_yet"))
#         return

#     if all(r["feasible"] for r in recipe_results):
#         st.success(get_text("all_feasible"))

#     selected_titles = st.multiselect(
#         get_text("select_recipes_label"),
#         [r["recipe"]["title"] for r in recipe_results],
#         format_func=lambda t: f"{t} {'✅' if next((r for r in recipe_results if r['recipe']['title'] == t), {}).get('feasible', False) else '❌'}"
#     )

#     selected_missing = []
#     for result in [r for r in recipe_results if r["recipe"]["title"] in selected_titles]:
#         st.markdown(f"#### {html.escape(result['recipe'].get('title', 'Untitled'))}")
#         if result["feasible"]:
#             st.success(get_text("all_available"))
#             if st.button(get_text("cook"), key=f"cook_{result['recipe'].get('id')}"):
#                 try:
#                     success, message = consume_ingredients_for_recipe(result["recipe"], user_id)
#                     if success:
#                         DatabaseManager.log_cooked_recipe(user_id, result["recipe"]["id"])
#                         count = DatabaseManager.get_cooked_count(user_id, result["recipe"]["id"])
#                         stars = calculate_stars(count, result["recipe"].get("is_signature", False))
#                         if stars > calculate_stars(count - 1, result["recipe"].get("is_signature", False)):
#                             st.success(get_text("congrats").format(stars="⭐" * stars, dish=result["recipe"]["title"]))
#                         st.success(message)
#                         st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                         st.rerun()
#                     else:
#                         st.error(message)
#                         _, shorts = recipe_feasibility(result["recipe"], user_id)
#                         if shorts:
#                             st.table([
#                                 {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
#                                  get_text("have"): f"{s['have_qty']} {s['have_unit']}",
#                                  get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
#                                 for s in shorts
#                             ])
#                 except SQLAlchemyError as e:
#                     logger.error(f"Error cooking recipe {result['recipe']['title']}: {e}")
#                     st.error(get_text("db_error").format(error=e))
#         else:
#             st.warning(get_text("missing_something"))
#             st.table([
#                 {get_text("name"): s["name"], get_text("need"): s["needed_qty"], get_text("have"): s["have_qty"],
#                  get_text("unit"): s["needed_unit"], get_text("missing"): s["missing_qty_disp"]}
#                 for s in result["shorts"]
#             ])
#             selected_missing.extend(result["shorts"])

#     if selected_missing and st.button(get_text("add_to_shopping")):
#         try:
#             agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
#             for s in selected_missing:
#                 key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
#                 agg_missing[key]["name"] = s["name"]
#                 agg_missing[key]["quantity"] += s["missing_qty_disp"]
#                 agg_missing[key]["unit"] = s["missing_unit_disp"]
#             st.session_state["shopping_list_data"] = list(agg_missing.values())
#             st.success(get_text("sent_to_shopping"))
#             st.rerun()
#         except SQLAlchemyError as e:
#             logger.error(f"Error adding to shopping list: {e}")
#             st.error(get_text("db_error").format(error=e))

# def shopping_list_page() -> None:
#     """Quản lý danh sách mua sắm và cập nhật kho."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Lỗi tải kho cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     shopping_list = st.session_state.get("shopping_list_data", [])
#     st.header(get_text("shopping_list"))
#     if not shopping_list:
#         st.info(get_text("empty_list"))
#         return

#     valid_shopping_list = []
#     for item in shopping_list:
#         if (
#             isinstance(item, dict) and
#             item.get("name") and isinstance(item.get("name"), str) and
#             isinstance(item.get("quantity"), (int, float)) and item["quantity"] >= 0 and
#             item.get("unit") and _norm_unit(item["unit"]) in [_norm_unit(u) for u in VALID_UNITS]
#         ):
#             valid_shopping_list.append(item)
#         else:
#             logger.warning(f"Invalid shopping list item: {item}")
#     shopping_list = valid_shopping_list
#     st.session_state["shopping_list_data"] = shopping_list

#     shopping_data = st.data_editor(
#         shopping_list,
#         column_config={
#             "name": st.column_config.TextColumn(get_text("name"), required=True),
#             "quantity": st.column_config.NumberColumn(get_text("quantity"), min_value=0.0, step=0.1, required=True),
#             "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#         },
#         num_rows="dynamic",
#         key="shopping_list_editor",
#         hide_index=True
#     )

#     st.session_state["shopping_list_data"] = shopping_data
#     purchased_labels = [f"{item['name']} ({item['unit']})" for item in shopping_data if item.get("name") and item.get("unit")]
#     purchased_names = st.multiselect(get_text("select_purchased"), options=purchased_labels)

#     if st.button(get_text("update_inventory")):
#         session = Session()
#         try:
#             for item in shopping_data:
#                 item_label = f"{item['name']} ({item['unit']})"
#                 if item_label in purchased_names:
#                     DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"])
#             st.session_state["shopping_list_data"] = [
#                 item for item in shopping_data if f"{item['name']} ({item['unit']})" not in purchased_names
#             ]
#             session.commit()
#             st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#             st.success(get_text("purchased"))
#             st.rerun()
#         except SQLAlchemyError as e:
#             session.rollback()
#             logger.error(f"Lỗi cập nhật kho từ danh sách mua sắm: {e}")
#             st.error(get_text("db_error").format(error=e))
#         finally:
#             session.close()

# def recipe_adjustment_page() -> None:
#     """Điều chỉnh công thức dựa trên khẩu phần hoặc nguyên liệu chính."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Lỗi tải dữ liệu cho điều chỉnh của người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     st.header(get_text("adjust_recipe"))
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Lỗi tải công thức cho người dùng {user_id}: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     if not recipes:
#         st.info(get_text("no_recipes"))
#         return

#     selected_recipe_title = st.selectbox(get_text("select_recipe"), [r.get("title") for r in recipes])
#     if not selected_recipe_title:
#         st.warning(get_text("no_recipe_selected"))
#         return

#     recipe = next(r for r in recipes if r.get("title") == selected_recipe_title)
#     adjustment_type = st.radio(get_text("adjustment_type"), [get_text("by_servings"), get_text("by_main_ingredient")])
#     adjustment_ratio = 1.0

#     if adjustment_type == get_text("by_servings"):
#         base_servings = float(recipe.get("servings", 1.0))
#         new_servings = st.number_input(get_text("new_servings"), min_value=0.1, step=0.1, value=base_servings)
#         adjustment_ratio = new_servings / base_servings if base_servings > 0 else 1.0
#     else:
#         main_ingredients = [ing for ing in recipe.get("ingredients", []) if not ing.get("is_spice")]
#         if not main_ingredients:
#             st.error(get_text("error_ingredients_required"))
#             return
#         main_ingredient = st.selectbox(get_text("main_ingredient"), [ing.get("name") for ing in main_ingredients])
#         selected_ing = next(ing for ing in main_ingredients if ing.get("name") == main_ingredient)
#         base_qty = float(selected_ing.get("quantity", 1.0))
#         new_quantity = st.number_input(get_text("new_quantity"), min_value=0.0, step=0.1, value=base_qty)
#         adjustment_ratio = new_quantity / base_qty if base_qty > 0 else 1.0

#     spice_display_to_key = {
#         get_text("mild"): "mild",
#         get_text("normal"): "normal",
#         get_text("rich"): "rich"
#     }
#     spice_level = st.radio(get_text("spice_level"), [get_text("mild"), get_text("normal"), get_text("rich")])
#     spice_key = spice_display_to_key.get(spice_level, "normal")
#     spice_factor = {"mild": 0.6, "normal": 0.8, "rich": 1.0}[spice_key]

#     adjusted_recipe = {
#         "id": recipe.get("id"),
#         "title": get_text("adjusted_recipe_title").format(title=recipe.get("title")),
#         "category": recipe.get("category"),
#         "instructions": recipe.get("instructions"),
#         "servings": (recipe.get("servings", 1.0) * adjustment_ratio) if adjustment_type == get_text("by_servings") else recipe.get("servings", 1.0),
#         "ingredients": [],
#         "origin_id": recipe.get("id"),
#         "tag": "adjusted"
#     }

#     for ing in recipe.get("ingredients", []):
#         new_qty = max(0.0, float(ing.get("quantity", 0.0)) * adjustment_ratio * (spice_factor if ing.get("is_spice") else 1.0))
#         adjusted_recipe["ingredients"].append({
#             "name": ing.get("name"),
#             "quantity": new_qty,
#             "unit": ing.get("unit"),
#             "is_spice": ing.get("is_spice", False)
#         })

#     st.session_state["adjusted_recipe"] = adjusted_recipe
#     st.subheader(get_text("adjusted_recipe"))
#     st.write(f"**{get_text('title')}:** {html.escape(adjusted_recipe['title'])}")
#     st.write(f"**{get_text('category')}:** {html.escape(adjusted_recipe.get('category', ''))}")
#     st.write(f"**{get_text('servings')}:** {float(adjusted_recipe.get('servings', 0.0)):.2f}")
#     st.write(f"**{get_text('instructions')}:** {html.escape(adjusted_recipe.get('instructions', ''))}")
#     st.table([
#         {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
#          get_text("unit"): ing["unit"], "Spice": "Yes" if ing["is_spice"] else "No"}
#         for ing in adjusted_recipe["ingredients"]
#     ])

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button(get_text("cook_adjusted")):
#             try:
#                 feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
#                 success, message = consume_ingredients_for_recipe(adjusted_recipe, user_id)
#                 if success:
#                     DatabaseManager.log_cooked_recipe(user_id, adjusted_recipe["origin_id"])
#                     count = DatabaseManager.get_cooked_count(user_id, adjusted_recipe["origin_id"])
#                     stars = calculate_stars(count, recipe.get("is_signature", False))
#                     if stars > calculate_stars(count - 1, recipe.get("is_signature", False)):
#                         st.success(get_text("congrats").format(stars="⭐" * stars, dish=adjusted_recipe["title"]))
#                     st.success(get_text("cook_adjusted_success").format(title=adjusted_recipe["title"]))
#                     st.session_state.pop("adjusted_recipe", None)
#                     st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                     st.rerun()
#                 else:
#                     st.error(get_text("cook_adjusted_failed").format(title=adjusted_recipe["title"], error=message.split(": ")[-1]))
#                     if shorts:
#                         st.table([
#                             {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
#                              get_text("have"): f"{s['have_qty']} {s['have_unit']}",
#                              get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
#                             for s in shorts
#                         ])
#             except SQLAlchemyError as e:
#                 logger.error(f"Error cooking adjusted recipe {adjusted_recipe['title']}: {e}")
#                 st.error(get_text("db_error").format(error=e))

#     with col2:
#         if st.button(get_text("add_to_shopping_adjusted")):
#             try:
#                 feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
#                 if not feasible:
#                     agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
#                     for s in shorts:
#                         key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
#                         agg_missing[key]["name"] = s["name"]
#                         agg_missing[key]["quantity"] += s["missing_qty_disp"]
#                         agg_missing[key]["unit"] = s["missing_unit_disp"]
#                     st.session_state["shopping_list_data"] = st.session_state.get("shopping_list_data", []) + list(agg_missing.values())
#                     st.success(get_text("sent_to_shopping"))
#                     st.rerun()
#             except SQLAlchemyError as e:
#                 logger.error(f"Error adding adjusted recipe to shopping list: {e}")
#                 st.error(get_text("db_error").format(error=e))

# def food_timeline_page() -> None:
#     """Hiển thị lịch sử nấu ăn dưới dạng dòng thời gian."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         history = DatabaseManager.list_cooked_history(user_id)
#         recipes = {r["id"]: r for r in DatabaseManager.list_recipes(user_id)}
#         st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Lỗi tải dữ liệu dòng thời gian: {e}")
#         st.error(get_text("db_error").format(error=e))
#         return

#     st.header(get_text("food_timeline"))
#     if not history:
#         st.info(get_text("no_history"))
#         return

#     recipe_counts = defaultdict(int)
#     for h in history:
#         recipe_counts[h["recipe_id"]] += 1

#     enriched = [
#         {
#             "date": h["cooked_date"],
#             "name": recipes[h["recipe_id"]]["title"],
#             "stars": calculate_stars(recipe_counts[h["recipe_id"]], recipes[h["recipe_id"]].get("is_signature", False)),
#             "recipe_id": h["recipe_id"],
#             "index": idx
#         }
#         for idx, h in enumerate(history) if h["recipe_id"] in recipes
#     ]

#     with st.form(key="timeline_search_form"):
#         search_query = st.text_input(get_text("search_placeholder"), value=st.session_state.get("search_value", ""), key="timeline_search_input")
#         if st.form_submit_button(get_text("reset_filter")):
#             st.session_state.search_value = ""
#             st.rerun()

#     tag_filter, week_filter, day_filter = None, None, None
#     if search_query:
#         if search_query.startswith("tag:"):
#             tag_filter = search_query[4:].strip().lower()
#         elif search_query.startswith(("tuần:", "week:")):
#             week_filter = search_query.split(":")[1].strip()
#         elif search_query.startswith(("ngày:", "day:")):
#             day_filter = search_query.split(":")[1].strip()
#         else:
#             keyword = search_query.lower()
#         st.session_state.search_value = search_query

#     filtered = enriched
#     if tag_filter:
#         filtered = [e for e in filtered if (tag_filter in ["signature", "món tủ"] and e["stars"] == 5) or (tag_filter == "exploring" and e["stars"] in (1, 2))]
#     if week_filter:
#         try:
#             week_num = int(week_filter)
#             start_week = datetime.now() - timedelta(weeks=week_num - 1, days=datetime.now().weekday())
#             end_week = start_week + timedelta(days=6)
#             filtered = [e for e in filtered if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]
#         except ValueError:
#             pass
#     if day_filter:
#         try:
#             day_date = datetime.strptime(day_filter, "%Y-%m-%d").date()
#             filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date() == day_date]
#         except ValueError:
#             pass
#     if search_query and not any([tag_filter, week_filter, day_filter]):
#         filtered = [e for e in filtered if search_query.lower() in e["name"].lower()]

#     if not filtered:
#         st.info(get_text("no_entries"))
#         return

#     filtered.sort(key=lambda e: e["date"], reverse=True)
#     current_date = datetime.now()
#     start_week = current_date - timedelta(days=current_date.weekday())
#     end_week = start_week + timedelta(days=6)
#     week_history = [e for e in enriched if start_week <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") <= end_week]

#     if week_history:
#         count = len(week_history)
#         most_dish = Counter(e["name"] for e in week_history).most_common(1)[0][0]
#         st.info(get_text("stats_week").format(count=count, dish=most_dish))

#     groups = defaultdict(list)
#     for e in filtered:
#         groups[datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date()].append(e)

#     for day in sorted(groups.keys(), reverse=True):
#         with st.container():
#             st.markdown('<div class="food-card">', unsafe_allow_html=True)
#             st.subheader(day.strftime("%Y-%m-%d"))
#             for e in groups[day]:
#                 col1, col2 = st.columns([5, 1])
#                 with col1:
#                     st.markdown(f"<span class='dish-name'>{html.escape(e['name'])}</span>", unsafe_allow_html=True)
#                 with col2:
#                     st.markdown(f"<span class='stars'>{'⭐' * e['stars']}</span>", unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

# def auth_gate_tabs() -> None:
#     """Hiển thị các tab xác thực cho đăng nhập, đăng ký và đặt lại mật khẩu."""
#     tabs = st.tabs([get_text("login"), get_text("register"), get_text("reset_password")])
#     with tabs[0]:
#         username = st.text_input(get_text("username"), key="login_username")
#         password = st.text_input(get_text("password"), type="password", key="login_password")
#         if st.button(get_text("login_button")):
#             try:
#                 user_id = DatabaseManager.verify_login(username, password)
#                 if user_id:
#                     st.session_state.update(user_id=user_id, username=username)
#                     st.success(get_text("login_button") + " successful!")
#                     st.rerun()
#                 else:
#                     st.error("Invalid username or password.")
#             except SQLAlchemyError as e:
#                 logger.error(f"Lỗi trong quá trình đăng nhập: {e}")
#                 st.error(get_text("db_error").format(error=e))
#     with tabs[1]:
#         username = st.text_input(get_text("username"), key="register_username")
#         password = st.text_input(get_text("password"), type="password", key="register_password")
#         sec_question = st.text_input(get_text("sec_question"), key="sec_question")
#         sec_answer = st.text_input(get_text("sec_answer"), type="password", key="sec_answer")
#         if st.button(get_text("create_account")):
#             try:
#                 success, message = DatabaseManager.create_user(username, password, sec_question, sec_answer)
#                 if success:
#                     st.success(message)
#                     user_id = DatabaseManager.verify_login(username, password)
#                     if user_id:
#                         st.session_state.update(user_id=user_id, username=username)
#                         st.rerun()
#                     else:
#                         st.error("Failed to log in after registration.")
#                 else:
#                     st.error(message)
#             except SQLAlchemyError as e:
#                 logger.error(f"Lỗi trong quá trình đăng ký: {e}")
#                 st.error(get_text("db_error").format(error=e))
#     with tabs[2]:
#         username = st.text_input(get_text("username"), key="reset_username")
#         sec_answer = st.text_input(get_text("sec_answer"), type="password", key="reset_sec_answer")
#         new_password = st.text_input(get_text("new_password"), type="password", key="reset_new_password")
#         if st.button(get_text("reset_button")):
#             try:
#                 success = DatabaseManager.reset_password(username, sec_answer, new_password)
#                 if success:
#                     st.success(get_text("reset_button") + " successful!")
#                     st.rerun()
#                 else:
#                     st.error("Invalid username or security answer.")
#             except SQLAlchemyError as e:
#                 logger.error(f"Lỗi trong quá trình đặt lại mật khẩu: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))















### tiếp tục chỉnh sửa Sử dụng bcrypt PostgreSQL








# import streamlit as st
# import html
# from datetime import datetime, timedelta
# from typing import Optional, Dict, List, Tuple, Any
# import logging
# from collections import defaultdict, Counter
# import re
# import bcrypt
# from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship, scoped_session
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.sql import func
# from dotenv import load_dotenv
# import os
# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# # Load environment variables
# load_dotenv()

# # Thiết lập logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# if not logger.handlers:
#     logger.addHandler(handler)

# # Constants
# APP_TITLE_EN = "RuaDen Recipe App"
# APP_TITLE_VI = "Ứng dụng Công thức RuaDen"
# VALID_UNITS = ["g", "kg", "ml", "l", "tsp", "tbsp", "cup", "piece", "pcs", "lạng", "chén", "bát"]

# # Database configuration
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/recipe_app")
# POSTGRES_SUPERUSER = os.getenv("POSTGRES_SUPERUSER", "postgres")
# POSTGRES_SUPERUSER_PASSWORD = os.getenv("POSTGRES_SUPERUSER_PASSWORD", "postgres")
# ROLE_NAME = "recipe_user"
# ROLE_PASSWORD = "secure_password_123"
# DB_NAME = "recipe_app"

# # Văn bản đa ngôn ngữ
# TEXT = {
#     "English": {
#         "app_title": APP_TITLE_EN,
#         "login": "🔐 Login",
#         "username": "Username",
#         "password": "Password",
#         "login_button": "Login",
#         "register": "🆕 Register",
#         "sec_question": "Security Question (for password reset)",
#         "sec_answer": "Security Answer",
#         "create_account": "Create Account",
#         "reset_password": "♻️ Reset Password",
#         "new_password": "New Password",
#         "reset_button": "Reset Password",
#         "logout": "Logout",
#         "language": "Language",
#         "title": "Title",
#         "category": "Category",
#         "instructions": "Instructions",
#         "servings": "Servings",
#         "name": "Name",
#         "quantity": "Quantity",
#         "unit": "Unit",
#         "need": "Need",
#         "have": "Have",
#         "missing": "Missing",
#         "inventory": "📦 Inventory",
#         "your_stock": "Your Stock",
#         "no_ingredients": "No ingredients yet.",
#         "unit_tips": "Unit tips: use g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
#         "add_ingredient": "Add New Ingredient",
#         "recipes": "📖 Recipes",
#         "your_recipes": "Your Recipes",
#         "no_recipes": "No recipes yet.",
#         "save_recipe": "Save Recipe",
#         "update_recipe": "Update Recipe",
#         "delete_recipe": "Delete Recipe",
#         "feasibility": "✅ Feasibility & Shopping",
#         "create_recipes_first": "Create recipes first.",
#         "you_can_cook": "Recipe Feasibility and Shopping List",
#         "none_yet": "None yet.",
#         "all_available": "All ingredients available.",
#         "cook": "Cook",
#         "missing_something": "Missing Ingredients",
#         "all_feasible": "All recipes are feasible 🎉",
#         "add_to_shopping": "Add missing to Shopping List",
#         "shopping_list": "🛒 Shopping List",
#         "empty_list": "Your shopping list is empty.",
#         "update_inventory": "Update Inventory from Shopping List",
#         "purchased": "Inventory updated with purchased items.",
#         "select_recipes_label": "Select recipes to proceed",
#         "select_purchased": "Select purchased items",
#         "sent_to_shopping": "Missing ingredients added to the shopping list.",
#         "cook_success": "Cooked successfully.",
#         "cook_failed": "Cooking failed: {error}",
#         "adjust_recipe": "⚖️ Adjust Recipe",
#         "select_recipe": "Select Recipe",
#         "adjustment_type": "Adjustment Type",
#         "by_servings": "By Servings",
#         "by_main_ingredient": "By Main Ingredient",
#         "new_servings": "New Servings",
#         "main_ingredient": "Main Ingredient",
#         "new_quantity": "New Quantity",
#         "spice_level": "Spice Adjustment",
#         "mild": "Mild (60%)",
#         "normal": "Normal (80%)",
#         "rich": "Rich (100%)",
#         "adjusted_recipe": "Adjusted Recipe",
#         "cook_adjusted": "Cook Adjusted Recipe",
#         "add_to_shopping_adjusted": "Add Missing to Shopping List",
#         "adjusted_recipe_title": "Adjusted: {title}",
#         "no_recipe_selected": "Please select a recipe to adjust.",
#         "invalid_adjustment": "Invalid adjustment parameters.",
#         "cook_adjusted_success": "Adjusted recipe '{title}' cooked successfully.",
#         "cook_adjusted_failed": "Failed to cook adjusted recipe '{title}': {error}",
#         "not_logged_in": "You must be logged in to access this page.",
#         "error_title_required": "Recipe title is required.",
#         "error_ingredients_required": "At least one valid ingredient (with name and positive quantity) is required.",
#         "duplicate_recipe": "A recipe with this title already exists.",
#         "error_invalid_name": "Invalid ingredient name: {name}",
#         "error_invalid_unit": "Invalid unit: {unit}",
#         "error_negative_qty": "Quantity must be positive for ingredient: {name}",
#         "save_success": "Recipe '{title}' saved successfully.",
#         "update_success": "Recipe '{title}' updated successfully.",
#         "delete_success": "Recipe '{title}' deleted successfully.",
#         "save_failed": "Failed to save recipe '{title}': {error}",
#         "update_failed": "Failed to update recipe '{title}': {error}",
#         "delete_failed": "Failed to delete recipe '{title}'.",
#         "food_timeline": "🍲 Food Timeline",
#         "no_history": "No cooking history yet.",
#         "no_entries": "No entries match the filters.",
#         "congrats": "Congratulations! You have reached {stars} with {dish} 🎉",
#         "signature_dish": "Signature Dish",
#         "search_placeholder": "Search (e.g., tag:signature, week:1, day:2025-09-01)",
#         "reset_filter": "🔄 Reset filter",
#         "stats_week": "This week you cooked {count} dishes, most frequent: {dish}",
#         "db_error": "Database error: {error}",
#         "save_changes": "Save Changes",
#         "inventory_updated": "Inventory updated successfully.",
#         "db_init_failed": "Failed to initialize database: {error}",
#         "invalid_quantity": "Invalid quantity format. Use numbers with optional decimal point or comma."
#     },
#     "Vietnamese": {
#         "app_title": APP_TITLE_VI,
#         "login": "🔐 Đăng nhập",
#         "username": "Tên người dùng",
#         "password": "Mật khẩu",
#         "login_button": "Đăng nhập",
#         "register": "🆕 Đăng ký",
#         "sec_question": "Câu hỏi bảo mật (để đặt lại mật khẩu)",
#         "sec_answer": "Câu trả lời bảo mật",
#         "create_account": "Tạo tài khoản",
#         "reset_password": "♻️ Đặt lại mật khẩu",
#         "new_password": "Mật khẩu mới",
#         "reset_button": "Đặt lại mật khẩu",
#         "logout": "Đăng xuất",
#         "language": "Ngôn ngữ",
#         "title": "Tiêu đề",
#         "category": "Danh mục",
#         "instructions": "Hướng dẫn",
#         "servings": "Khẩu phần",
#         "name": "Tên",
#         "quantity": "Số lượng",
#         "unit": "Đơn vị",
#         "need": "Cần",
#         "have": "Có",
#         "missing": "Thiếu",
#         "inventory": "📦 Kho",
#         "your_stock": "Kho của bạn",
#         "no_ingredients": "Chưa có nguyên liệu.",
#         "unit_tips": "Mẹo đơn vị: sử dụng g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
#         "add_ingredient": "Thêm nguyên liệu mới",
#         "recipes": "📖 Công thức",
#         "your_recipes": "Công thức của bạn",
#         "no_recipes": "Chưa có công thức.",
#         "save_recipe": "Lưu công thức",
#         "update_recipe": "Cập nhật công thức",
#         "delete_recipe": "Xóa công thức",
#         "feasibility": "✅ Tính khả thi & Mua sắm",
#         "create_recipes_first": "Vui lòng tạo công thức trước.",
#         "you_can_cook": "Tính khả thi công thức và danh sách mua sắm",
#         "none_yet": "Chưa có.",
#         "all_available": "Tất cả nguyên liệu đều có sẵn.",
#         "cook": "Nấu",
#         "missing_something": "Thiếu nguyên liệu",
#         "all_feasible": "Tất cả công thức đều khả thi 🎉",
#         "add_to_shopping": "Thêm nguyên liệu thiếu vào danh sách mua sắm",
#         "shopping_list": "🛒 Danh sách mua sắm",
#         "empty_list": "Danh sách mua sắm của bạn trống.",
#         "update_inventory": "Cập nhật kho từ danh sách mua sắm",
#         "purchased": "Kho đã được cập nhật với các mặt hàng đã mua.",
#         "select_recipes_label": "Chọn công thức để tiếp tục",
#         "select_purchased": "Chọn các mặt hàng đã mua",
#         "sent_to_shopping": "Nguyên liệu thiếu đã được thêm vào danh sách mua sắm.",
#         "cook_success": "Nấu thành công.",
#         "cook_failed": "Nấu thất bại: {error}",
#         "adjust_recipe": "⚖️ Điều chỉnh công thức",
#         "select_recipe": "Chọn công thức",
#         "adjustment_type": "Loại điều chỉnh",
#         "by_servings": "Theo khẩu phần",
#         "by_main_ingredient": "Theo nguyên liệu chính",
#         "new_servings": "Khẩu phần mới",
#         "main_ingredient": "Nguyên liệu chính",
#         "new_quantity": "Số lượng mới",
#         "spice_level": "Điều chỉnh độ cay",
#         "mild": "Nhẹ (60%)",
#         "normal": "Bình thường (80%)",
#         "rich": "Đậm (100%)",
#         "adjusted_recipe": "Công thức đã điều chỉnh",
#         "cook_adjusted": "Nấu công thức đã điều chỉnh",
#         "add_to_shopping_adjusted": "Thêm nguyên liệu thiếu vào danh sách mua sắm",
#         "adjusted_recipe_title": "Đã điều chỉnh: {title}",
#         "no_recipe_selected": "Vui lòng chọn một công thức để điều chỉnh.",
#         "invalid_adjustment": "Tham số điều chỉnh không hợp lệ.",
#         "cook_adjusted_success": "Công thức điều chỉnh '{title}' đã nấu thành công.",
#         "cook_adjusted_failed": "Không thể nấu công thức điều chỉnh '{title}': {error}",
#         "not_logged_in": "Bạn phải đăng nhập để truy cập trang này.",
#         "error_title_required": "Tiêu đề công thức là bắt buộc.",
#         "error_ingredients_required": "Cần ít nhất một nguyên liệu hợp lệ (với tên và số lượng dương).",
#         "duplicate_recipe": "Công thức với tiêu đề này đã tồn tại.",
#         "error_invalid_name": "Tên nguyên liệu không hợp lệ: {name}",
#         "error_invalid_unit": "Đơn vị không hợp lệ: {unit}",
#         "error_negative_qty": "Số lượng phải dương cho nguyên liệu: {name}",
#         "save_success": "Công thức '{title}' đã được lưu thành công.",
#         "update_success": "Công thức '{title}' đã được cập nhật thành công.",
#         "delete_success": "Công thức '{title}' đã được xóa thành công.",
#         "save_failed": "Không thể lưu công thức '{title}': {error}",
#         "update_failed": "Không thể cập nhật công thức '{title}': {error}",
#         "delete_failed": "Không thể xóa công thức '{title}'.",
#         "food_timeline": "🍲 Dòng thời gian món ăn",
#         "no_history": "Chưa có lịch sử nấu ăn.",
#         "no_entries": "Không có mục nào khớp với bộ lọc.",
#         "congrats": "Chúc mừng! Bạn đã đạt được {stars} với món {dish} 🎉",
#         "signature_dish": "Món tủ",
#         "search_placeholder": "Tìm kiếm (ví dụ: tag:signature, week:1, day:2025-09-01)",
#         "reset_filter": "🔄 Đặt lại bộ lọc",
#         "stats_week": "Tuần này bạn đã nấu {count} món, món thường xuyên nhất: {dish}",
#         "db_error": "Lỗi cơ sở dữ liệu: {error}",
#         "save_changes": "Save Changes",
#         "inventory_updated": "Inventory updated successfully.",
#         "db_init_failed": "Failed to initialize database: {error}",
#         "invalid_quantity": "Invalid quantity format. Use numbers with optional decimal point or comma."
#     }
# }

# # Database initialization
# def initialize_database() -> bool:
#     """Initialize PostgreSQL database and role if they don't exist."""
#     try:
#         conn = psycopg2.connect(
#             dbname="postgres",
#             user=POSTGRES_SUPERUSER,
#             password=POSTGRES_SUPERUSER_PASSWORD,
#             host="localhost",
#             port=5432
#         )
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (ROLE_NAME,))
#             if not cursor.fetchone():
#                 cursor.execute(f"CREATE ROLE {ROLE_NAME} WITH LOGIN PASSWORD %s", (ROLE_PASSWORD,))
#                 logger.info(f"Created PostgreSQL role: {ROLE_NAME}")
#             cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
#             if not cursor.fetchone():
#                 cursor.execute(f"CREATE DATABASE {DB_NAME}")
#                 cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {ROLE_NAME}")
#                 logger.info(f"Created PostgreSQL database: {DB_NAME}")
#         conn.close()
#         return True
#     except Exception as e:
#         logger.error(f"Failed to initialize database: {e}")
#         return False

# # Database setup
# try:
#     if not initialize_database():
#         st.error(get_text("db_init_failed").format(error="Could not initialize database. Check logs for details."))
#         st.stop()
#     engine = create_engine(DATABASE_URL, echo=False)
#     Base = declarative_base()
#     Session = scoped_session(sessionmaker(bind=engine))
# except Exception as e:
#     logger.error(f"Failed to connect to database: {e}")
#     st.error(get_text("db_error").format(error=str(e)))
#     st.stop()

# # Database Models
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     username = Column(String(255), unique=True, nullable=False)
#     password_hash = Column(String(128), nullable=False)
#     sec_question = Column(String(255), nullable=False)
#     sec_answer_hash = Column(String(128), nullable=False)
#     inventory = relationship("Inventory", back_populates="user")
#     recipes = relationship("Recipe", back_populates="user")
#     cooked_history = relationship("CookedHistory", back_populates="user")

# class Inventory(Base):
#     __tablename__ = "inventory"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     name = Column(String(255), nullable=False)
#     quantity = Column(Float, nullable=False)
#     unit = Column(String(50), nullable=False)
#     user = relationship("User", back_populates="inventory")

# class Recipe(Base):
#     __tablename__ = "recipes"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     title = Column(String(255), nullable=False)
#     category = Column(String(255))
#     instructions = Column(Text)
#     servings = Column(Float, default=1.0)
#     is_signature = Column(Boolean, default=False)
#     user = relationship("User", back_populates="recipes")
#     ingredients = relationship("RecipeIngredient", back_populates="recipe")

# class RecipeIngredient(Base):
#     __tablename__ = "recipe_ingredients"
#     id = Column(Integer, primary_key=True)
#     recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
#     name = Column(String(255), nullable=False)
#     quantity = Column(Float, nullable=False)
#     unit = Column(String(50), nullable=False)
#     is_spice = Column(Boolean, default=False)
#     recipe = relationship("Recipe", back_populates="ingredients")

# class CookedHistory(Base):
#     __tablename__ = "cooked_history"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
#     cooked_date = Column(DateTime, default=func.now())
#     user = relationship("User", back_populates="cooked_history")

# try:
#     Base.metadata.create_all(engine)
# except Exception as e:
#     logger.error(f"Failed to create tables: {e}")
#     st.error(get_text("db_error").format(error=str(e)))
#     st.stop()

# # Danh sách export
# __all__ = [
#     'inject_css', 'get_text', 'current_user_id', 'initialize_session_state',
#     'topbar_account', 'inventory_page', 'recipes_page', 'feasibility_page',
#     'shopping_list_page', 'recipe_adjustment_page', 'food_timeline_page',
#     'auth_gate_tabs', 'main'
# ]

# def inject_css() -> None:
#     """Inject custom CSS for Streamlit app styling."""
#     try:
#         st.markdown(
#             """
#             <style>
#                 .block-container {
#                     padding-top: 5rem;
#                     padding-bottom: 2rem;
#                     max-width: 980px;
#                 }
#                 .stTextInput > div > div > input,
#                 .stNumberInput > div > div > input,
#                 textarea {
#                     border-radius: 12px !important;
#                     border: 1px solid #e6e6e6 !important;
#                     padding: .55rem .8rem !important;
#                 }
#                 .stButton > button {
#                     background: #111 !important;
#                     color: #fff !important;
#                     border: none !important;
#                     border-radius: 14px !important;
#                     padding: .55rem 1rem !important;
#                     font-weight: 500 !important;
#                     transition: transform .12s ease, opacity .12s ease;
#                 }
#                 .stButton > button:hover {
#                     transform: translateY(-1px);
#                     opacity: .95;
#                 }
#                 table {
#                     border-collapse: collapse;
#                     width: 100%;
#                 }
#                 th, td {
#                     padding: 8px 10px;
#                     border-bottom: 1px solid #eee;
#                 }
#                 th {
#                     color: #666;
#                     font-weight: 600;
#                 }
#                 td {
#                     color: #222;
#                 }
#                 .stTabs [data-baseweb="tab-list"] {
#                     gap: .25rem;
#                     margin-top: 1rem;
#                 }
#                 .stTabs [data-baseweb="tab"] {
#                     padding: .6rem 1rem;
#                 }
#                 .streamlit-expanderHeader {
#                     font-weight: 600;
#                 }
#                 #topbar-account {
#                     margin-bottom: 1rem;
#                 }
#                 .food-card {
#                     border: 1px solid #eee;
#                     border-radius: 12px;
#                     padding: 1rem;
#                     margin-bottom: 1rem;
#                     background-color: #f9f9f9;
#                 }
#                 .dish-name {
#                     font-weight: bold;
#                     font-size: 1.2em;
#                 }
#                 .stars {
#                     font-size: 1.2em;
#                     color: #FFD700;
#                     text-align: right;
#                 }
#                 @media (max-width: 600px) {
#                     .block-container {
#                         padding-top: 4rem;
#                         padding-left: 1rem;
#                         padding-right: 1rem;
#                     }
#                     .stButton > button {
#                         width: 100%;
#                         margin-bottom: 0.5rem;
#                     }
#                     .stTabs [data-baseweb="tab-list"] {
#                         margin-top: 0.5rem;
#                     }
#                 }
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )
#     except Exception as e:
#         logger.error(f"Error injecting CSS: {e}")
#         st.error("Cannot apply custom styling. Continuing with default.")

# def get_text(key: str, **kwargs) -> str:
#     """Retrieve multilingual text with safe formatting."""
#     lang = st.session_state.get("language", "English")
#     template = TEXT.get(lang, TEXT["English"]).get(key, key)
#     if kwargs:
#         try:
#             return template.format(**kwargs)
#         except Exception as e:
#             logger.warning(f"i18n fallback for key='{key}': {e}")
#             return template
#     return template

# def current_user_id() -> Optional[int]:
#     """Get current user ID from session state."""
#     return st.session_state.get("user_id")

# def initialize_session_state() -> None:
#     """Initialize session state with default values."""
#     defaults = {
#         "user_id": None,
#         "username": None,
#         "language": "English",
#         "editing_recipe_id": None,
#         "recipe_form_data": {
#             "title": "",
#             "category": "",
#             "instructions": "",
#             "is_signature": False,
#             "servings": 1.0,
#             "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#         },
#         "shopping_list_data": [],
#         "adjusted_recipe": None,
#         "search_value": ""
#     }
#     for key, value in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = value

# def topbar_account() -> None:
#     """Display top bar with username, language selector, and logout button."""
#     user_id = current_user_id()
#     if not user_id:
#         return
#     with st.container():
#         st.markdown('<div id="topbar-account">', unsafe_allow_html=True)
#         col1, col2, col3 = st.columns([3, 1, 1])
#         with col1:
#             st.write(f"{get_text('username')}: {html.escape(st.session_state.get('username', 'Unknown'))}")
#         with col2:
#             st.selectbox(
#                 get_text("language"),
#                 ["English", "Vietnamese"],
#                 index=0 if st.session_state.get("language", "English") == "English" else 1,
#                 key="language_selector",
#                 on_change=lambda: st.session_state.update({"language": st.session_state.language_selector})
#             )
#         with col3:
#             if st.button(get_text("logout")):
#                 st.session_state.clear()
#                 initialize_session_state()
#                 logger.info(f"User {st.session_state.get('username', 'Unknown')} logged out")
#                 st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)

# def calculate_stars(count: int, is_signature: bool) -> int:
#     """Calculate stars based on cook count and signature status."""
#     if not isinstance(count, int) or count < 0:
#         return 0
#     thresholds = [(15, 5), (8, 4), (5, 3), (3, 2), (1, 1)]
#     return 5 if is_signature else next((stars for threshold, stars in thresholds if count >= threshold), 0)

# def _norm_name(name: str) -> str:
#     """Normalize ingredient name for comparison."""
#     return (name or "").strip().lower()

# def _norm_unit(unit: str) -> str:
#     """Normalize unit for comparison."""
#     return (unit or "").strip().lower()

# def _inventory_map(user_id: int) -> Dict[Tuple[str, str], dict]:
#     """Create inventory map based on normalized name and unit."""
#     with Session() as session:
#         try:
#             items = session.query(Inventory).filter_by(user_id=user_id).all()
#             return {
#                 (_norm_name(item.name), _norm_unit(item.unit)): {
#                     "id": item.id,
#                     "name": item.name,
#                     "quantity": item.quantity,
#                     "unit": item.unit
#                 }
#                 for item in items if item.name and item.unit
#             }
#         except SQLAlchemyError as e:
#             logger.error(f"Error fetching inventory map for user {user_id}: {e}")
#             raise

# def validate_ingredients(recipe: Dict, inventory_map: Dict[Tuple[str, str], dict]) -> Tuple[bool, Optional[str]]:
#     """Validate recipe ingredients and check feasibility against inventory."""
#     if not recipe.get("ingredients"):
#         return False, get_text("error_ingredients_required")
    
#     for ing in recipe.get("ingredients", []):
#         name = _norm_name(ing.get("name", ""))
#         unit = _norm_unit(ing.get("unit", ""))
#         qty = float(ing.get("quantity", 0.0))
        
#         if not name or qty <= 0:
#             return False, get_text("error_ingredients_required")
#         if not DatabaseManager.validate_name(ing.get("name", "")):
#             return False, get_text("error_invalid_name").format(name=ing.get("name"))
#         if unit not in [_norm_unit(u) for u in VALID_UNITS]:
#             return False, get_text("error_invalid_unit").format(unit=ing.get("unit"))
        
#         key = (name, unit)
#         inv_item = inventory_map.get(key)
#         if not inv_item:
#             return False, f"Ingredient {ing.get('name')} not found in inventory"
#         if inv_item["unit"] != ing.get("unit"):
#             return False, f"Unit mismatch for {ing.get('name')}: expected {ing.get('unit')}, found {inv_item['unit']}"
#         if inv_item["quantity"] < qty:
#             return False, f"Insufficient quantity for {ing.get('name')}: need {qty}, have {inv_item['quantity']}"
    
#     return True, None

# def recipe_feasibility(recipe: Dict, user_id: int) -> Tuple[bool, List[Dict]]:
#     """Check recipe feasibility based on inventory."""
#     try:
#         inv_map = _inventory_map(user_id)
#         shorts = []
#         feasible = True
        
#         for ing in recipe.get("ingredients", []):
#             name = _norm_name(ing.get("name", ""))
#             unit = _norm_unit(ing.get("unit", ""))
#             qty = float(ing.get("quantity", 0.0))
#             key = (name, unit)
#             inv_item = inv_map.get(key, {})
#             have_qty = float(inv_item.get("quantity", 0.0))
#             missing = max(0.0, qty - have_qty)
            
#             if missing > 1e-9 or not inv_item:
#                 feasible = False
#                 shorts.append({
#                     "name": ing.get("name", ""),
#                     "needed_qty": qty,
#                     "have_qty": have_qty,
#                     "needed_unit": ing.get("unit", ""),
#                     "have_unit": inv_item.get("unit", "") if inv_item else "",
#                     "missing_qty_disp": missing,
#                     "missing_unit_disp": ing.get("unit", "")
#                 })
        
#         return feasible, shorts
#     except SQLAlchemyError as e:
#         logger.error(f"Error checking recipe feasibility: {e}")
#         raise

# def consume_ingredients_for_recipe(recipe: Dict, user_id: int) -> Tuple[bool, str]:
#     """Consume ingredients from inventory if recipe is feasible."""
#     with Session() as session:
#         try:
#             inv_map = _inventory_map(user_id)
#             is_valid, error = validate_ingredients(recipe, inv_map)
#             if not is_valid:
#                 logger.warning(f"Validation failed for recipe {recipe.get('title', 'Unknown')}: {error}")
#                 return False, get_text("cook_failed").format(error=error)
            
#             for ing in recipe.get("ingredients", []):
#                 name = _norm_name(ing.get("name", ""))
#                 unit = _norm_unit(ing.get("unit", ""))
#                 qty = float(ing.get("quantity", 0.0))
#                 key = (name, unit)
#                 inv_item = inv_map.get(key)
                
#                 if not inv_item:
#                     raise ValueError(f"Ingredient {ing.get('name')} not found in inventory")
#                 if inv_item["unit"] != ing.get("unit"):
#                     raise ValueError(f"Unit mismatch for {ing.get('name')}")
#                 if inv_item["quantity"] < qty:
#                     raise ValueError(f"Insufficient quantity for {ing.get('name')}")
                
#                 inventory_item = session.query(Inventory).filter_by(id=inv_item["id"]).first()
#                 inventory_item.quantity = max(0.0, inventory_item.quantity - qty)
            
#             session.commit()
#             logger.info(f"Successfully consumed ingredients for recipe {recipe.get('title', 'Unknown')}")
#             return True, get_text("cook_success")
#         except Exception as e:
#             session.rollback()
#             logger.error(f"Failed to consume ingredients for recipe {recipe.get('title', 'Unknown')}: {str(e)}")
#             return False, get_text("cook_failed").format(error=str(e))

# def normalize_quantity(quantity: Any) -> float:
#     """Normalize quantity input to float, handling strings with commas or decimals."""
#     if isinstance(quantity, (int, float)):
#         return float(quantity)
#     if isinstance(quantity, str):
#         try:
#             return float(quantity.replace(',', '.').strip())
#         except ValueError:
#             raise ValueError(get_text("invalid_quantity"))
#     raise ValueError(get_text("invalid_quantity"))

# class DatabaseManager:
#     @staticmethod
#     def validate_name(name: str) -> bool:
#         """Validate ingredient or user name, allowing Unicode characters."""
#         return bool(name and name.strip() and all(c.isprintable() for c in name))

#     @staticmethod
#     def normalize_name(name: str) -> str:
#         """Normalize name for comparison."""
#         return _norm_name(name)

#     @classmethod
#     def verify_login(cls, username: str, password: str) -> Optional[int]:
#         """Verify user login credentials."""
#         if not username or not password or len(password) < 8:
#             return None
#         with Session() as session:
#             try:
#                 user = session.query(User).filter_by(username=username).first()
#                 if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
#                     return user.id
#                 return None
#             except SQLAlchemyError as e:
#                 logger.error(f"Error verifying login for {username}: {e}")
#                 raise

#     @classmethod
#     def create_user(cls, username: str, password: str, sec_question: str, sec_answer: str) -> Tuple[bool, str]:
#         """Create a new user."""
#         if not all([username.strip(), password.strip(), sec_question.strip(), sec_answer.strip()]):
#             return False, "All fields required."
#         if len(password) < 8:
#             return False, "Password must be at least 8 characters."
#         if not cls.validate_name(username):
#             return False, get_text("error_invalid_name").format(name=username)
        
#         with Session() as session:
#             try:
#                 if session.query(User).filter_by(username=username).first():
#                     return False, "Username already exists."
#                 password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 sec_answer_hash = bcrypt.hashpw(sec_answer.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 user = User(
#                     username=username,
#                     password_hash=password_hash,
#                     sec_question=sec_question,
#                     sec_answer_hash=sec_answer_hash
#                 )
#                 session.add(user)
#                 session.commit()
#                 logger.info(f"Created user: {username}")
#                 return True, "User created successfully."
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error creating user {username}: {e}")
#                 return False, get_text("db_error").format(error=str(e))

#     @classmethod
#     def reset_password(cls, username: str, sec_answer: str, new_password: str) -> bool:
#         """Reset user password."""
#         if not all([username.strip(), sec_answer.strip(), new_password.strip()]):
#             return False
#         if len(new_password) < 8:
#             return False
#         with Session() as session:
#             try:
#                 user = session.query(User).filter_by(username=username).first()
#                 if not user:
#                     return False
#                 if bcrypt.checkpw(sec_answer.encode('utf-8'), user.sec_answer_hash.encode('utf-8')):
#                     user.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                     session.commit()
#                     logger.info(f"Password reset for user: {username}")
#                     return True
#                 return False
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error resetting password for {username}: {e}")
#                 return False

#     @classmethod
#     def list_inventory(cls, user_id: int) -> List[Dict]:
#         """List user inventory."""
#         with Session() as session:
#             try:
#                 items = session.query(Inventory).filter_by(user_id=user_id).all()
#                 return [
#                     {"id": item.id, "name": item.name, "quantity": item.quantity, "unit": item.unit}
#                     for item in items
#                 ]
#             except SQLAlchemyError as e:
#                 logger.error(f"Error listing inventory for user {user_id}: {e}")
#                 raise

#     @classmethod
#     def upsert_inventory(cls, user_id: int, name: str, quantity: float, unit: str) -> bool:
#         """Add or update inventory item."""
#         with Session() as session:
#             try:
#                 if not cls.validate_name(name):
#                     logger.error(f"Invalid name for inventory item: {name}")
#                     return False
#                 if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                     logger.error(f"Invalid unit for inventory item: {unit}")
#                     return False
#                 if quantity < 0:
#                     logger.error(f"Negative quantity for inventory item: {name}")
#                     return False
#                 item = session.query(Inventory).filter_by(
#                     user_id=user_id,
#                     name=cls.normalize_name(name),
#                     unit=_norm_unit(unit)
#                 ).first()
#                 if item:
#                     item.quantity = max(0.0, item.quantity + quantity)
#                 else:
#                     item = Inventory(
#                         user_id=user_id,
#                         name=name,
#                         quantity=max(0.0, quantity),
#                         unit=unit
#                     )
#                     session.add(item)
#                 session.commit()
#                 logger.info(f"Upserted inventory item: {name} for user {user_id}")
#                 return True
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error upserting inventory for user {user_id}: {e}")
#                 return False

#     @classmethod
#     def update_inventory_item(cls, user_id: int, item_id: int, name: str, quantity: float, unit: str) -> Tuple[bool, str]:
#         """Update specific inventory item by ID."""
#         with Session() as session:
#             try:
#                 item = session.query(Inventory).filter_by(id=item_id, user_id=user_id).first()
#                 if not item:
#                     logger.error(f"Inventory item not found: id={item_id}, user_id={user_id}")
#                     return False, "Item not found."
#                 if not cls.validate_name(name):
#                     logger.error(f"Invalid name for inventory item: {name}")
#                     return False, get_text("error_invalid_name").format(name=name)
#                 if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                     logger.error(f"Invalid unit for inventory item: {unit}")
#                     return False, get_text("error_invalid_unit").format(unit=unit)
#                 if quantity < 0:
#                     logger.error(f"Negative quantity for inventory item: {name}")
#                     return False, get_text("error_negative_qty").format(name=name)
#                 item.name = name
#                 item.quantity = max(0.0, quantity)
#                 item.unit = unit
#                 session.commit()
#                 logger.info(f"Updated inventory item: id={item_id} for user {user_id}")
#                 return True, "Inventory item updated successfully."
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error updating inventory item {item_id}: {e}")
#                 return False, get_text("db_error").format(error=str(e))

#     @classmethod
#     def delete_inventory(cls, user_id: int, item_id: int) -> bool:
#         """Delete inventory item by ID."""
#         with Session() as session:
#             try:
#                 item = session.query(Inventory).filter_by(id=item_id, user_id=user_id).first()
#                 if item:
#                     session.delete(item)
#                     session.commit()
#                     logger.info(f"Deleted inventory item: id={item_id} for user {user_id}")
#                     return True
#                 return False
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error deleting inventory item {item_id}: {e}")
#                 return False

#     @classmethod
#     def list_recipes(cls, user_id: int) -> List[Dict]:
#         """List user recipes."""
#         with Session() as session:
#             try:
#                 recipes = session.query(Recipe).filter_by(user_id=user_id).all()
#                 return [
#                     {
#                         "id": r.id,
#                         "title": r.title,
#                         "category": r.category,
#                         "instructions": r.instructions,
#                         "servings": r.servings,
#                         "is_signature": r.is_signature,
#                         "ingredients": [
#                             {
#                                 "name": i.name,
#                                 "quantity": i.quantity,
#                                 "unit": i.unit,
#                                 "is_spice": i.is_spice
#                             } for i in r.ingredients
#                         ]
#                     } for r in recipes
#                 ]
#             except SQLAlchemyError as e:
#                 logger.error(f"Error listing recipes for user {user_id}: {e}")
#                 raise

#     @classmethod
#     def create_recipe(cls, user_id: int, title: str, category: str, instructions: str, 
#                      ingredients: List[Dict], recipe_id: Optional[int] = None, is_signature: bool = False) -> Tuple[bool, str]:
#         """Create or update a recipe."""
#         with Session() as session:
#             try:
#                 if not title.strip():
#                     return False, get_text("error_title_required")
#                 if not any(ing["name"].strip() and ing["quantity"] > 0 for ing in ingredients):
#                     return False, get_text("error_ingredients_required")
                
#                 if session.query(Recipe).filter_by(user_id=user_id, title=title).filter(Recipe.id != recipe_id).first():
#                     return False, get_text("duplicate_recipe")
                
#                 if recipe_id:
#                     recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
#                     if not recipe:
#                         return False, get_text("delete_failed").format(title=title)
#                     recipe.title = title
#                     recipe.category = category
#                     recipe.instructions = instructions
#                     recipe.is_signature = is_signature
#                     recipe.servings = 1.0
#                     session.query(RecipeIngredient).filter_by(recipe_id=recipe_id).delete()
#                 else:
#                     recipe = Recipe(
#                         user_id=user_id,
#                         title=title,
#                         category=category,
#                         instructions=instructions,
#                         servings=1.0,
#                         is_signature=is_signature
#                     )
#                     session.add(recipe)
#                     session.flush()
                
#                 for ing in ingredients:
#                     if not cls.validate_name(ing["name"]):
#                         return False, get_text("error_invalid_name").format(name=ing["name"])
#                     if _norm_unit(ing["unit"]) not in [_norm_unit(u) for u in VALID_UNITS]:
#                         return False, get_text("error_invalid_unit").format(unit=ing["unit"])
#                     if ing["quantity"] <= 0:
#                         return False, get_text("error_negative_qty").format(name=ing["name"])
#                     session.add(RecipeIngredient(
#                         recipe_id=recipe.id,
#                         name=ing["name"],
#                         quantity=ing["quantity"],
#                         unit=ing["unit"],
#                         is_spice=ing.get("is_spice", False)
#                     ))
                
#                 session.commit()
#                 logger.info(f"{'Updated' if recipe_id else 'Created'} recipe: {title} for user {user_id}")
#                 return True, get_text("update_success" if recipe_id else "save_success").format(title=title)
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error saving recipe {title}: {e}")
#                 return False, get_text("save_failed").format(title=title, error=str(e))

#     @classmethod
#     def delete_recipe(cls, user_id: int, recipe_id: int) -> bool:
#         """Delete a recipe."""
#         with Session() as session:
#             try:
#                 recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
#                 if recipe:
#                     session.delete(recipe)
#                     session.commit()
#                     logger.info(f"Deleted recipe: id={recipe_id} for user {user_id}")
#                     return True
#                 return False
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error deleting recipe {recipe_id}: {e}")
#                 return False

#     @classmethod
#     def log_cooked_recipe(cls, user_id: int, recipe_id: int) -> bool:
#         """Log a cooked recipe."""
#         with Session() as session:
#             try:
#                 session.add(CookedHistory(user_id=user_id, recipe_id=recipe_id))
#                 session.commit()
#                 logger.info(f"Logged cooked recipe: id={recipe_id} for user {user_id}")
#                 return True
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error logging cooked recipe {recipe_id}: {e}")
#                 return False

#     @classmethod
#     def list_cooked_history(cls, user_id: int) -> List[Dict]:
#         """List cooking history."""
#         with Session() as session:
#             try:
#                 history = session.query(CookedHistory).filter_by(user_id=user_id).all()
#                 return [
#                     {"recipe_id": h.recipe_id, "cooked_date": h.cooked_date.strftime("%Y-%m-%d %H:%M:%S")}
#                     for h in history
#                 ]
#             except SQLAlchemyError as e:
#                 logger.error(f"Error listing cooked history for user {user_id}: {e}")
#                 raise

#     @classmethod
#     def get_cooked_count(cls, user_id: int, recipe_id: int) -> int:
#         """Get count of times a recipe was cooked."""
#         with Session() as session:
#             try:
#                 return session.query(CookedHistory).filter_by(user_id=user_id, recipe_id=recipe_id).count()
#             except SQLAlchemyError as e:
#                 logger.error(f"Error getting cooked count for recipe {recipe_id}: {e}")
#                 raise

# def inventory_page() -> None:
#     """Display and manage ingredient inventory."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading inventory for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     st.header(get_text("inventory"))
#     st.subheader(get_text("your_stock"))
#     st.caption(get_text("unit_tips"))

#     with st.expander(get_text("add_ingredient")):
#         with st.form(key="add_inventory_form"):
#             col1, col2, col3 = st.columns([2, 1, 1])
#             with col1:
#                 ingredient_name = st.text_input(get_text("name"), placeholder=get_text("e.g., chicken"), key="new_ingredient_name")
#             with col2:
#                 quantity_input = st.text_input(get_text("quantity"), value="0.0", key="new_quantity")
#             with col3:
#                 unit = st.selectbox(get_text("unit"), options=VALID_UNITS, key="new_unit")
#             if st.form_submit_button(get_text("add_ingredient")):
#                 try:
#                     quantity = normalize_quantity(quantity_input)
#                     if not ingredient_name.strip():
#                         st.error(get_text("error_ingredients_required"))
#                     elif not DatabaseManager.validate_name(ingredient_name):
#                         st.error(get_text("error_invalid_name").format(name=ingredient_name))
#                     elif _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                         st.error(get_text("error_invalid_unit").format(unit=unit))
#                     elif quantity < 0:
#                         st.error(get_text("error_negative_qty").format(name=ingredient_name))
#                     else:
#                         if DatabaseManager.upsert_inventory(user_id, ingredient_name.strip(), quantity, unit):
#                             st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                             st.success(get_text("save_success").format(title=ingredient_name))
#                             st.rerun()
#                         else:
#                             st.error(get_text("save_failed").format(title=ingredient_name, error="Could not add ingredient"))
#                 except ValueError as e:
#                     st.error(str(e))
#                 except SQLAlchemyError as e:
#                     logger.error(f"Error adding ingredient {ingredient_name}: {e}")
#                     st.error(get_text("db_error").format(error=str(e)))

#     edited_data = st.data_editor(
#         inventory,
#         column_config={
#             "id": None,
#             "name": st.column_config.TextColumn(get_text("name"), required=True),
#             "quantity": st.column_config.NumberColumn(
#                 get_text("quantity"),
#                 min_value=0.0,
#                 format="%.2f",
#                 required=True
#             ),
#             "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#         },
#         num_rows="dynamic",
#         key=f"inventory_editor_{user_id}",
#         hide_index=True
#     )

#     if st.button(get_text("save_changes")):
#         errors = []
#         validated_data = []
#         for item in edited_data:
#             name = item.get("name", "").strip()
#             unit = item.get("unit", "")
#             quantity = item.get("quantity")
#             if not name or quantity is None or not unit:
#                 errors.append(get_text("error_ingredients_required"))
#                 continue
#             if not DatabaseManager.validate_name(name):
#                 errors.append(get_text("error_invalid_name").format(name=name))
#                 continue
#             if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                 errors.append(get_text("error_invalid_unit").format(unit=unit))
#                 continue
#             if quantity < 0:
#                 errors.append(get_text("error_negative_qty").format(name=name))
#                 continue
#             validated_data.append({"id": item.get("id"), "name": name, "quantity": float(quantity), "unit": unit})

#         if errors:
#             for error in errors:
#                 st.error(error)
#         else:
#             try:
#                 old_ids = {item.get("id") for item in inventory if item.get("id")}
#                 edited_ids = {item.get("id") for item in validated_data if item.get("id")}
#                 deleted_ids = old_ids - edited_ids
#                 for item_id in deleted_ids:
#                     if DatabaseManager.delete_inventory(user_id, item_id):
#                         logger.info(f"Deleted inventory item: id={item_id} for user {user_id}")
#                 for item in validated_data:
#                     if item.get("id"):
#                         success, message = DatabaseManager.update_inventory_item(user_id, item["id"], item["name"], item["quantity"], item["unit"])
#                         if not success:
#                             st.error(message)
#                             continue
#                     else:
#                         if not DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"]):
#                             st.error(get_text("save_failed").format(title=item["name"], error="Could not add ingredient"))
#                             continue
#                 st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                 st.success(get_text("inventory_updated"))
#                 st.rerun()
#             except SQLAlchemyError as e:
#                 logger.error(f"Error updating inventory: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

#     if not inventory:
#         st.info(get_text("no_ingredients"))

# def recipes_page() -> None:
#     """Display and manage user recipes."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading recipes for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     st.header(get_text("recipes"))
#     st.subheader(get_text("your_recipes"))
#     st.caption(get_text("unit_tips"))

#     if not recipes:
#         st.info(get_text("no_recipes"))

#     form_data = st.session_state.recipe_form_data
#     recipe_id = st.session_state.get("editing_recipe_id")

#     with st.form(key="recipe_form"):
#         title = st.text_input(get_text("title"), value=form_data["title"], key="recipe_title")
#         category = st.text_input(get_text("category"), value=form_data["category"], key="recipe_category")
#         instructions = st.text_area(get_text("instructions"), value=form_data["instructions"], key="recipe_instructions")
#         is_signature = st.checkbox(get_text("signature_dish"), value=form_data["is_signature"], key="recipe_is_signature")
#         ingredients_data = st.data_editor(
#             form_data["ingredients"],
#             column_config={
#                 "name": st.column_config.TextColumn(get_text("name"), required=True),
#                 "quantity": st.column_config.NumberColumn(
#                     get_text("quantity"),
#                     min_value=0.0,
#                     format="%.2f",
#                     required=True
#                 ),
#                 "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#                 "is_spice": st.column_config.CheckboxColumn("Spice", default=False)
#             },
#             num_rows="dynamic",
#             key="ingredients_editor",
#             hide_index=True
#         )

#         submit_label = get_text("update_recipe") if recipe_id else get_text("save_recipe")
#         if st.form_submit_button(submit_label):
#             if not title.strip():
#                 st.error(get_text("error_title_required"))
#                 return
#             valid_ingredients = []
#             for ing in ingredients_data:
#                 name = ing.get("name", "").strip()
#                 quantity = ing.get("quantity")
#                 unit = ing.get("unit", "")
#                 is_spice = ing.get("is_spice", False)
#                 if not name or quantity is None or not unit:
#                     st.error(get_text("error_ingredients_required"))
#                     return
#                 if not DatabaseManager.validate_name(name):
#                     st.error(get_text("error_invalid_name").format(name=name))
#                     return
#                 if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                     st.error(get_text("error_invalid_unit").format(unit=unit))
#                     return
#                 if quantity <= 0:
#                     st.error(get_text("error_negative_qty").format(name=name))
#                     return
#                 valid_ingredients.append({
#                     "name": name,
#                     "quantity": float(quantity),
#                     "unit": unit,
#                     "is_spice": is_spice
#                 })
#             if not valid_ingredients:
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             existing_recipe = next((r for r in recipes if r.get("title") == title.strip() and r.get("id") != recipe_id), None)
#             if existing_recipe:
#                 st.error(get_text("duplicate_recipe"))
#                 return
#             try:
#                 success, message = DatabaseManager.create_recipe(
#                     user_id, title.strip(), category.strip(), instructions.strip(), 
#                     valid_ingredients, recipe_id, is_signature
#                 )
#                 if success:
#                     st.success(message)
#                     st.session_state.recipe_form_data = {
#                         "title": "",
#                         "category": "",
#                         "instructions": "",
#                         "is_signature": False,
#                         "servings": 1.0,
#                         "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#                     }
#                     st.session_state.editing_recipe_id = None
#                     st.rerun()
#                 else:
#                     st.error(message)
#             except SQLAlchemyError as e:
#                 logger.error(f"Error saving recipe {title}: {e}")
#                 st.error(get_text("save_failed").format(title=title, error=str(e)))

#     if recipes:
#         for recipe in recipes:
#             signature_text = f" - {get_text('signature_dish')}" if recipe.get("is_signature") else ""
#             with st.expander(f"{html.escape(recipe.get('title', 'Untitled'))} ({html.escape(recipe.get('category', '-'))}) {signature_text}"):
#                 st.write(f"**{get_text('instructions')}:** {html.escape(recipe.get('instructions', ''))}")
#                 st.table([
#                     {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
#                      get_text("unit"): ing["unit"], "Spice": "Yes" if ing.get("is_spice") else "No"}
#                     for ing in recipe.get("ingredients", [])
#                 ])
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button(get_text("update_recipe"), key=f"edit_{recipe.get('id')}"):
#                         st.session_state.editing_recipe_id = recipe["id"]
#                         st.session_state.recipe_form_data = {
#                             "title": recipe["title"],
#                             "category": recipe["category"],
#                             "instructions": recipe["instructions"],
#                             "is_signature": recipe.get("is_signature", False),
#                             "servings": recipe.get("servings", 1.0),
#                             "ingredients": [
#                                 {"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": ing.get("is_spice", False)}
#                                 for ing in recipe.get("ingredients", [])
#                             ]
#                         }
#                         st.rerun()
#                 with col2:
#                     if st.button(get_text("delete_recipe"), key=f"delete_{recipe.get('id')}"):
#                         try:
#                             if DatabaseManager.delete_recipe(user_id, recipe["id"]):
#                                 st.success(get_text("delete_success").format(title=recipe["title"]))
#                                 st.rerun()
#                             else:
#                                 st.error(get_text("delete_failed").format(title=recipe["title"]))
#                         except SQLAlchemyError as e:
#                             logger.error(f"Error deleting recipe {recipe['title']}: {e}")
#                             st.error(get_text("delete_failed").format(title=recipe["title"]))

# def feasibility_page() -> None:
#     """Display recipe feasibility and shopping list options."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading data for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     if not recipes:
#         st.info(get_text("create_recipes_first"))
#         return

#     st.header(get_text("feasibility"))
#     st.subheader(get_text("you_can_cook"))

#     recipe_results = [
#         {"recipe": r, "feasible": feasible, "shorts": shorts}
#         for r in recipes
#         for feasible, shorts in [recipe_feasibility(r, user_id)]
#     ]

#     if not recipe_results:
#         st.info(get_text("none_yet"))
#         return

#     if all(r["feasible"] for r in recipe_results):
#         st.success(get_text("all_feasible"))

#     selected_titles = st.multiselect(
#         get_text("select_recipes_label"),
#         [r["recipe"]["title"] for r in recipe_results],
#         format_func=lambda t: f"{t} {'✅' if next((r for r in recipe_results if r['recipe']['title'] == t), {}).get('feasible', False) else '❌'}"
#     )

#     selected_missing = []
#     for result in [r for r in recipe_results if r["recipe"]["title"] in selected_titles]:
#         st.markdown(f"#### {html.escape(result['recipe'].get('title', 'Untitled'))}")
#         if result["feasible"]:
#             st.success(get_text("all_available"))
#             if st.button(get_text("cook"), key=f"cook_{result['recipe'].get('id')}"):
#                 try:
#                     success, message = consume_ingredients_for_recipe(result["recipe"], user_id)
#                     if success:
#                         DatabaseManager.log_cooked_recipe(user_id, result["recipe"]["id"])
#                         count = DatabaseManager.get_cooked_count(user_id, result["recipe"]["id"])
#                         stars = calculate_stars(count, result["recipe"].get("is_signature", False))
#                         if stars > calculate_stars(count - 1, result["recipe"].get("is_signature", False)):
#                             st.success(get_text("congrats").format(stars="⭐" * stars, dish=result["recipe"]["title"]))
#                         st.success(message)
#                         st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                         st.rerun()
#                     else:
#                         st.error(message)
#                         _, shorts = recipe_feasibility(result["recipe"], user_id)
#                         if shorts:
#                             st.table([
#                                 {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
#                                  get_text("have"): f"{s['have_qty']} {s['have_unit']}",
#                                  get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
#                                 for s in shorts
#                             ])
#                 except SQLAlchemyError as e:
#                     logger.error(f"Error cooking recipe {result['recipe']['title']}: {e}")
#                     st.error(get_text("db_error").format(error=str(e)))
#         else:
#             st.warning(get_text("missing_something"))
#             st.table([
#                 {get_text("name"): s["name"], get_text("need"): s["needed_qty"], get_text("have"): s["have_qty"],
#                  get_text("unit"): s["needed_unit"], get_text("missing"): s["missing_qty_disp"]}
#                 for s in result["shorts"]
#             ])
#             selected_missing.extend(result["shorts"])

#     if selected_missing and st.button(get_text("add_to_shopping")):
#         try:
#             agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
#             for s in selected_missing:
#                 key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
#                 agg_missing[key]["name"] = s["name"]
#                 agg_missing[key]["quantity"] += s["missing_qty_disp"]
#                 agg_missing[key]["unit"] = s["missing_unit_disp"]
#             st.session_state["shopping_list_data"] = list(agg_missing.values())
#             st.success(get_text("sent_to_shopping"))
#             st.rerun()
#         except SQLAlchemyError as e:
#             logger.error(f"Error adding to shopping list: {e}")
#             st.error(get_text("db_error").format(error=str(e)))

# def shopping_list_page() -> None:
#     """Manage shopping list and update inventory."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading inventory for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     shopping_list = st.session_state.get("shopping_list_data", [])
#     st.header(get_text("shopping_list"))
#     if not shopping_list:
#         st.info(get_text("empty_list"))
#         return

#     valid_shopping_list = []
#     for item in shopping_list:
#         try:
#             quantity = normalize_quantity(item.get("quantity", 0.0))
#             if (isinstance(item, dict) and
#                     item.get("name") and isinstance(item.get("name"), str) and
#                     quantity >= 0 and
#                     item.get("unit") and _norm_unit(item["unit"]) in [_norm_unit(u) for u in VALID_UNITS]):
#                 valid_shopping_list.append({
#                     "name": item["name"],
#                     "quantity": quantity,
#                     "unit": item["unit"]
#                 })
#             else:
#                 logger.warning(f"Invalid shopping list item: {item}")
#         except ValueError as e:
#             logger.warning(f"Invalid quantity in shopping list item: {item}, error: {e}")
#     shopping_list = valid_shopping_list
#     st.session_state["shopping_list_data"] = shopping_list

#     shopping_data = st.data_editor(
#         shopping_list,
#         column_config={
#             "name": st.column_config.TextColumn(get_text("name"), required=True),
#             "quantity": st.column_config.NumberColumn(
#                 get_text("quantity"),
#                 min_value=0.0,
#                 format="%.2f",
#                 required=True
#             ),
#             "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#         },
#         num_rows="dynamic",
#         key="shopping_list_editor",
#         hide_index=True
#     )

#     validated_shopping_data = []
#     for item in shopping_data:
#         name = item.get("name", "").strip()
#         quantity = item.get("quantity")
#         unit = item.get("unit", "")
#         if not name or quantity is None or not unit:
#             st.error(get_text("error_ingredients_required"))
#             return
#         if not DatabaseManager.validate_name(name):
#             st.error(get_text("error_invalid_name").format(name=name))
#             return
#         if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#             st.error(get_text("error_invalid_unit").format(unit=unit))
#             return
#         if quantity < 0:
#             st.error(get_text("error_negative_qty").format(name=name))
#             return
#         validated_shopping_data.append({
#             "name": name,
#             "quantity": float(quantity),
#             "unit": unit
#         })
#     st.session_state["shopping_list_data"] = validated_shopping_data

#     purchased_labels = [f"{item['name']} ({item['unit']})" for item in validated_shopping_data if item.get("name") and item.get("unit")]
#     purchased_names = st.multiselect(get_text("select_purchased"), options=purchased_labels)

#     if st.button(get_text("update_inventory")):
#         with Session() as session:
#             try:
#                 for item in validated_shopping_data:
#                     item_label = f"{item['name']} ({item['unit']})"
#                     if item_label in purchased_names:
#                         if not DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"]):
#                             st.error(get_text("save_failed").format(title=item["name"], error="Could not update inventory"))
#                             continue
#                 st.session_state["shopping_list_data"] = [
#                     item for item in validated_shopping_data if f"{item['name']} ({item['unit']})" not in purchased_names
#                 ]
#                 session.commit()
#                 st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                 st.success(get_text("purchased"))
#                 st.rerun()
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error updating inventory from shopping list: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

# def recipe_adjustment_page() -> None:
#     """Adjust recipes based on servings or main ingredient."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading data for adjustment for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     st.header(get_text("adjust_recipe"))
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading recipes for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     if not recipes:
#         st.info(get_text("no_recipes"))
#         return

#     selected_recipe_title = st.selectbox(get_text("select_recipe"), [r.get("title") for r in recipes])
#     if not selected_recipe_title:
#         st.warning(get_text("no_recipe_selected"))
#         return

#     recipe = next(r for r in recipes if r.get("title") == selected_recipe_title)
#     adjustment_type = st.radio(get_text("adjustment_type"), [get_text("by_servings"), get_text("by_main_ingredient")])
#     adjustment_ratio = 1.0

#     try:
#         if adjustment_type == get_text("by_servings"):
#             base_servings = float(recipe.get("servings", 1.0))
#             new_servings = st.number_input(get_text("new_servings"), min_value=0.1, step=0.1, value=base_servings)
#             adjustment_ratio = new_servings / base_servings if base_servings > 0 else 1.0
#         else:
#             main_ingredients = [ing for ing in recipe.get("ingredients", []) if not ing.get("is_spice")]
#             if not main_ingredients:
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             main_ingredient = st.selectbox(get_text("main_ingredient"), [ing.get("name") for ing in main_ingredients])
#             selected_ing = next(ing for ing in main_ingredients if ing.get("name") == main_ingredient)
#             base_qty = float(selected_ing.get("quantity", 1.0))
#             new_quantity = st.number_input(get_text("new_quantity"), min_value=0.0, step=0.1, value=base_qty)
#             adjustment_ratio = new_quantity / base_qty if base_qty > 0 else 1.0
#     except ValueError as e:
#         st.error(get_text("invalid_quantity"))
#         return

#     spice_display_to_key = {
#         get_text("mild"): "mild",
#         get_text("normal"): "normal",
#         get_text("rich"): "rich"
#     }
#     spice_level = st.radio(get_text("spice_level"), [get_text("mild"), get_text("normal"), get_text("rich")])
#     spice_key = spice_display_to_key.get(spice_level, "normal")
#     spice_factor = {"mild": 0.6, "normal": 0.8, "rich": 1.0}[spice_key]

#     adjusted_recipe = {
#         "id": recipe.get("id"),
#         "title": get_text("adjusted_recipe_title").format(title=recipe.get("title")),
#         "category": recipe.get("category"),
#         "instructions": recipe.get("instructions"),
#         "servings": (recipe.get("servings", 1.0) * adjustment_ratio) if adjustment_type == get_text("by_servings") else recipe.get("servings", 1.0),
#         "ingredients": [],
#         "origin_id": recipe.get("id"),
#         "tag": "adjusted"
#     }

#     for ing in recipe.get("ingredients", []):
#         try:
#             new_qty = max(0.0, float(ing.get("quantity", 0.0)) * adjustment_ratio * (spice_factor if ing.get("is_spice") else 1.0))
#             adjusted_recipe["ingredients"].append({
#                 "name": ing.get("name"),
#                 "quantity": new_qty,
#                 "unit": ing.get("unit"),
#                 "is_spice": ing.get("is_spice", False)
#             })
#         except ValueError:
#             st.error(get_text("invalid_quantity"))
#             return

#     st.session_state["adjusted_recipe"] = adjusted_recipe
#     st.subheader(get_text("adjusted_recipe"))
#     st.write(f"**{get_text('title')}:** {html.escape(adjusted_recipe['title'])}")
#     st.write(f"**{get_text('category')}:** {html.escape(adjusted_recipe.get('category', ''))}")
#     st.write(f"**{get_text('servings')}:** {float(adjusted_recipe.get('servings', 0.0)):.2f}")
#     st.write(f"**{get_text('instructions')}:** {html.escape(adjusted_recipe.get('instructions', ''))}")
#     st.table([
#         {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
#          get_text("unit"): ing["unit"], "Spice": "Yes" if ing["is_spice"] else "No"}
#         for ing in adjusted_recipe["ingredients"]
#     ])

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button(get_text("cook_adjusted")):
#             try:
#                 feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
#                 success, message = consume_ingredients_for_recipe(adjusted_recipe, user_id)
#                 if success:
#                     DatabaseManager.log_cooked_recipe(user_id, adjusted_recipe["origin_id"])
#                     count = DatabaseManager.get_cooked_count(user_id, adjusted_recipe["origin_id"])
#                     stars = calculate_stars(count, recipe.get("is_signature", False))
#                     if stars > calculate_stars(count - 1, recipe.get("is_signature", False)):
#                         st.success(get_text("congrats").format(stars="⭐" * stars, dish=adjusted_recipe["title"]))
#                     st.success(get_text("cook_adjusted_success").format(title=adjusted_recipe["title"]))
#                     st.session_state.pop("adjusted_recipe", None)
#                     st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                     st.rerun()
#                 else:
#                     st.error(get_text("cook_adjusted_failed").format(title=adjusted_recipe["title"], error=message.split(": ")[-1]))
#                     if shorts:
#                         st.table([
#                             {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
#                              get_text("have"): f"{s['have_qty']} {s['have_unit']}",
#                              get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
#                             for s in shorts
#                         ])
#             except SQLAlchemyError as e:
#                 logger.error(f"Error cooking adjusted recipe {adjusted_recipe['title']}: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

#     with col2:
#         if st.button(get_text("add_to_shopping_adjusted")):
#             try:
#                 feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
#                 if not feasible:
#                     agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
#                     for s in shorts:
#                         key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
#                     agg_missing[key]["name"] = s["missing_unit_disp"]
#                     agg_missing[key]["quantity"] += s["missing_qty_disp"]
#                     agg_missing[key]["unit"] = s["missing_unit_disp"]
#                     new_shopping_list = list(agg_missing.values())
#                     st.session_state["shopping_list_data"] = new_shopping_list
#                     st.success(get_text("sent_to_shopping"))
#                     st.rerun()
#                 else:
#                     st.info(get_text("all_available"))
#             except SQLAlchemyError as e:
#                 logger.error(f"Error adding adjusted recipe to shopping list: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

# def food_timeline_page() -> None:
#     """Display cooking history as a timeline."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#         history = DatabaseManager.list_cooked_history(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading data for timeline for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     st.header(get_text("food_timeline"))
#     if not history:
#         st.info(get_text("no_history"))
#         return

#     recipe_map = {r["id"]: r for r in recipes}
#     search = st.text_input(get_text("search_placeholder"), key="timeline_search", value=st.session_state.get("search_value", ""))
#     st.session_state["search_value"] = search

#     filtered_history = []
#     for entry in history:
#         recipe = recipe_map.get(entry["recipe_id"], {"title": "Unknown", "is_signature": False})
#         count = DatabaseManager.get_cooked_count(user_id, entry["recipe_id"])
#         stars = calculate_stars(count, recipe.get("is_signature", False))
#         entry_data = {
#             "recipe_id": entry["recipe_id"],
#             "title": recipe["title"],
#             "cooked_date": entry["cooked_date"],
#             "stars": stars,
#             "is_signature": recipe.get("is_signature", False)
#         }
#         if not search:
#             filtered_history.append(entry_data)
#         else:
#             search_lower = search.lower()
#             date = datetime.strptime(entry["cooked_date"], "%Y-%m-%d %H:%M:%S")
#             week = date.isocalendar()[1]
#             searches = [s.strip() for s in search_lower.split(",")]
#             match = False
#             for s in searches:
#                 if s.startswith("tag:signature") and entry_data["is_signature"]:
#                     match = True
#                 elif s.startswith("week:") and s[5:].isdigit() and int(s[5:]) == week:
#                     match = True
#                 elif s.startswith("day:") and s[4:] in entry["cooked_date"]:
#                     match = True
#                 elif search_lower in entry_data["title"].lower():
#                     match = True
#             if match:
#                 filtered_history.append(entry_data)

#     if not filtered_history:
#         st.info(get_text("no_entries"))
#         return

#     if st.button(get_text("reset_filter")):
#         st.session_state["search_value"] = ""
#         st.rerun()

#     dish_counts = Counter(h["title"] for h in filtered_history)
#     if dish_counts:
#         week_start = datetime.now() - timedelta(days=datetime.now().weekday())
#         week_end = week_start + timedelta(days=6)
#         week_history = [
#             h for h in filtered_history
#             if week_start <= datetime.strptime(h["cooked_date"], "%Y-%m-%d %H:%M:%S") <= week_end
#         ]
#         week_counts = Counter(h["title"] for h in week_history)
#         most_common = week_counts.most_common(1)
#         if most_common:
#             st.write(get_text("stats_week").format(
#                 count=len(week_history),
#                 dish=most_common[0][0]
#             ))

#     for entry in sorted(filtered_history, key=lambda x: x["cooked_date"], reverse=True):
#         with st.container():
#             st.markdown('<div class="food-card">', unsafe_allow_html=True)
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.markdown(f'<span class="dish-name">{html.escape(entry["title"])}</span>', unsafe_allow_html=True)
#                 st.write(f"{entry['cooked_date']}")
#             with col2:
#                 st.markdown(f'<span class="stars">{"⭐" * entry["stars"]}</span>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

# def auth_gate_tabs() -> None:
#     """Display authentication tabs for login, register, and reset password."""
#     tabs = st.tabs([get_text("login"), get_text("register"), get_text("reset_password")])
#     with tabs[0]:
#         with st.form(key="login_form"):
#             username = st.text_input(get_text("username"), key="login_username")
#             password = st.text_input(get_text("password"), type="password", key="login_password")
#             if st.form_submit_button(get_text("login_button")):
#                 user_id = DatabaseManager.verify_login(username, password)
#                 if user_id:
#                     st.session_state["user_id"] = user_id
#                     st.session_state["username"] = username
#                     logger.info(f"User {username} logged in successfully")
#                     st.success(f"Welcome, {username}!")
#                     st.rerun()
#                 else:
#                     st.error("Invalid username or password")
#     with tabs[1]:
#         with st.form(key="register_form"):
#             username = st.text_input(get_text("username"), key="register_username")
#             password = st.text_input(get_text("password"), type="password", key="register_password")
#             sec_question = st.text_input(get_text("sec_question"), key="register_sec_question")
#             sec_answer = st.text_input(get_text("sec_answer"), type="password", key="register_sec_answer")
#             if st.form_submit_button(get_text("create_account")):
#                 success, message = DatabaseManager.create_user(username, password, sec_question, sec_answer)
#                 if success:
#                     st.success(message)
#                     user_id = DatabaseManager.verify_login(username, password)
#                     if user_id:
#                         st.session_state["user_id"] = user_id
#                         st.session_state["username"] = username
#                         logger.info(f"User {username} registered and logged in")
#                         st.rerun()
#                 else:
#                     st.error(message)
#     with tabs[2]:
#         with st.form(key="reset_form"):
#             username = st.text_input(get_text("username"), key="reset_username")
#             sec_answer = st.text_input(get_text("sec_answer"), type="password", key="reset_sec_answer")
#             new_password = st.text_input(get_text("new_password"), type="password", key="reset_new_password")
#             if st.form_submit_button(get_text("reset_button")):
#                 if DatabaseManager.reset_password(username, sec_answer, new_password):
#                     st.success("Password reset successfully")
#                     logger.info(f"Password reset for user {username}")
#                 else:
#                     st.error("Invalid username or security answer")

# def main() -> None:
#     """Main application entry point."""
#     st.set_page_config(page_title=APP_TITLE_EN, page_icon="🍽️", layout="wide")
#     inject_css()
#     initialize_session_state()

#     lang = st.session_state.get("language", "English")
#     st.title(get_text("app_title"))

#     if not current_user_id():
#         auth_gate_tabs()
#     else:
#         topbar_account()
#         tabs = st.tabs([
#             get_text("inventory"),
#             get_text("recipes"),
#             get_text("feasibility"),
#             get_text("shopping_list"),
#             get_text("adjust_recipe"),
#             get_text("food_timeline")
#         ])
#         with tabs[0]:
#             inventory_page()
#         with tabs[1]:
#             recipes_page()
#         with tabs[2]:
#             feasibility_page()
#         with tabs[3]:
#             shopping_list_page()
#         with tabs[4]:
#             recipe_adjustment_page()
#         with tabs[5]:
#             food_timeline_page()

# if __name__ == "__main__":
#     main()


##### đang tiếp tục test 

# import streamlit as st
# import html
# from datetime import datetime, timedelta
# from typing import Optional, Dict, List, Tuple, Any
# import logging
# from collections import defaultdict, Counter
# import re
# import bcrypt
# from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship, scoped_session
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.sql import func
# from dotenv import load_dotenv
# import os
# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# # Load environment variables
# load_dotenv()

# # Thiết lập logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# if not logger.handlers:
#     logger.addHandler(handler)

# # Constants
# APP_TITLE_EN = "RuaDen Recipe App"
# APP_TITLE_VI = "Ứng dụng Công thức RuaDen"
# VALID_UNITS = ["g", "kg", "ml", "l", "tsp", "tbsp", "cup", "piece", "pcs", "lạng", "chén", "bát"]

# # Database configuration
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/recipe_app")
# POSTGRES_SUPERUSER = os.getenv("POSTGRES_SUPERUSER", "postgres")
# POSTGRES_SUPERUSER_PASSWORD = os.getenv("POSTGRES_SUPERUSER_PASSWORD", "postgres")
# ROLE_NAME = "recipe_user"
# ROLE_PASSWORD = "secure_password_123"
# DB_NAME = "recipe_app"

# # Văn bản đa ngôn ngữ
# TEXT = {
#     "English": {
#         "app_title": APP_TITLE_EN,
#         "login": "🔐 Login",
#         "username": "Username",
#         "password": "Password",
#         "login_button": "Login",
#         "register": "🆕 Register",
#         "sec_question": "Security Question (for password reset)",
#         "sec_answer": "Security Answer",
#         "create_account": "Create Account",
#         "reset_password": "♻️ Reset Password",
#         "new_password": "New Password",
#         "reset_button": "Reset Password",
#         "logout": "Logout",
#         "language": "Language",
#         "title": "Title",
#         "category": "Category",
#         "instructions": "Instructions",
#         "servings": "Servings",
#         "name": "Name",
#         "quantity": "Quantity",
#         "unit": "Unit",
#         "need": "Need",
#         "have": "Have",
#         "missing": "Missing",
#         "inventory": "📦 Inventory",
#         "your_stock": "Your Stock",
#         "no_ingredients": "No ingredients yet.",
#         "unit_tips": "Unit tips: use g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
#         "add_ingredient": "Add New Ingredient",
#         "recipes": "📖 Recipes",
#         "your_recipes": "Your Recipes",
#         "no_recipes": "No recipes yet.",
#         "save_recipe": "Save Recipe",
#         "update_recipe": "Update Recipe",
#         "delete_recipe": "Delete Recipe",
#         "feasibility": "✅ Feasibility & Shopping",
#         "create_recipes_first": "Create recipes first.",
#         "you_can_cook": "Recipe Feasibility and Shopping List",
#         "none_yet": "None yet.",
#         "all_available": "All ingredients available.",
#         "cook": "Cook",
#         "missing_something": "Missing Ingredients",
#         "all_feasible": "All recipes are feasible 🎉",
#         "add_to_shopping": "Add missing to Shopping List",
#         "shopping_list": "🛒 Shopping List",
#         "empty_list": "Your shopping list is empty.",
#         "update_inventory": "Update Inventory from Shopping List",
#         "purchased": "Inventory updated with purchased items.",
#         "select_recipes_label": "Select recipes to proceed",
#         "select_purchased": "Select purchased items",
#         "sent_to_shopping": "Missing ingredients added to the shopping list.",
#         "cook_success": "Cooked successfully.",
#         "cook_failed": "Cooking failed: {error}",
#         "adjust_recipe": "⚖️ Adjust Recipe",
#         "select_recipe": "Select Recipe",
#         "adjustment_type": "Adjustment Type",
#         "by_servings": "By Servings",
#         "by_main_ingredient": "By Main Ingredient",
#         "new_servings": "New Servings",
#         "main_ingredient": "Main Ingredient",
#         "new_quantity": "New Quantity",
#         "spice_level": "Spice Adjustment",
#         "mild": "Mild (60%)",
#         "normal": "Normal (80%)",
#         "rich": "Rich (100%)",
#         "adjusted_recipe": "Adjusted Recipe",
#         "cook_adjusted": "Cook Adjusted Recipe",
#         "add_to_shopping_adjusted": "Add Missing to Shopping List",
#         "adjusted_recipe_title": "Adjusted: {title}",
#         "no_recipe_selected": "Please select a recipe to adjust.",
#         "invalid_adjustment": "Invalid adjustment parameters.",
#         "cook_adjusted_success": "Adjusted recipe '{title}' cooked successfully.",
#         "cook_adjusted_failed": "Failed to cook adjusted recipe '{title}': {error}",
#         "not_logged_in": "You must be logged in to access this page.",
#         "error_title_required": "Recipe title is required.",
#         "error_ingredients_required": "At least one valid ingredient (with name and positive quantity) is required.",
#         "duplicate_recipe": "A recipe with this title already exists.",
#         "error_invalid_name": "Invalid ingredient name: {name}",
#         "error_invalid_unit": "Invalid unit: {unit}",
#         "error_negative_qty": "Quantity must be positive for ingredient: {name}",
#         "save_success": "Recipe '{title}' saved successfully.",
#         "update_success": "Recipe '{title}' updated successfully.",
#         "delete_success": "Recipe '{title}' deleted successfully.",
#         "save_failed": "Failed to save recipe '{title}': {error}",
#         "update_failed": "Failed to update recipe '{title}': {error}",
#         "delete_failed": "Failed to delete recipe '{title}'.",
#         "food_timeline": "🍲 Food Timeline",
#         "no_history": "No cooking history yet.",
#         "no_entries": "No entries match the filters.",
#         "congrats": "Congratulations! You have reached {stars} with {dish} 🎉",
#         "signature_dish": "Signature Dish",
#         "search_placeholder": "Search (e.g., tag:signature, week:1, day:2025-09-01)",
#         "reset_filter": "🔄 Reset filter",
#         "stats_week": "This week you cooked {count} dishes, most frequent: {dish}",
#         "db_error": "Database error: {error}",
#         "save_changes": "Save Changes",
#         "inventory_updated": "Inventory updated successfully.",
#         "db_init_failed": "Failed to initialize database: {error}",
#         "invalid_quantity": "Invalid quantity format. Use numbers with optional decimal point or comma."
#     },
#     "Vietnamese": {
#         "app_title": APP_TITLE_VI,
#         "login": "🔐 Đăng nhập",
#         "username": "Tên người dùng",
#         "password": "Mật khẩu",
#         "login_button": "Đăng nhập",
#         "register": "🆕 Đăng ký",
#         "sec_question": "Câu hỏi bảo mật (để đặt lại mật khẩu)",
#         "sec_answer": "Câu trả lời bảo mật",
#         "create_account": "Tạo tài khoản",
#         "reset_password": "♻️ Đặt lại mật khẩu",
#         "new_password": "Mật khẩu mới",
#         "reset_button": "Đặt lại mật khẩu",
#         "logout": "Đăng xuất",
#         "language": "Ngôn ngữ",
#         "title": "Tiêu đề",
#         "category": "Danh mục",
#         "instructions": "Hướng dẫn",
#         "servings": "Khẩu phần",
#         "name": "Tên",
#         "quantity": "Số lượng",
#         "unit": "Đơn vị",
#         "need": "Cần",
#         "have": "Có",
#         "missing": "Thiếu",
#         "inventory": "📦 Kho",
#         "your_stock": "Kho của bạn",
#         "no_ingredients": "Chưa có nguyên liệu.",
#         "unit_tips": "Mẹo đơn vị: sử dụng g, kg, ml, l, tsp, tbsp, cup, piece, pcs, lạng, chén, bát.",
#         "add_ingredient": "Thêm nguyên liệu mới",
#         "recipes": "📖 Công thức",
#         "your_recipes": "Công thức của bạn",
#         "no_recipes": "Chưa có công thức.",
#         "save_recipe": "Lưu công thức",
#         "update_recipe": "Cập nhật công thức",
#         "delete_recipe": "Xóa công thức",
#         "feasibility": "✅ Tính khả thi & Mua sắm",
#         "create_recipes_first": "Vui lòng tạo công thức trước.",
#         "you_can_cook": "Tính khả thi công thức và danh sách mua sắm",
#         "none_yet": "Chưa có.",
#         "all_available": "Tất cả nguyên liệu đều có sẵn.",
#         "cook": "Nấu",
#         "missing_something": "Thiếu nguyên liệu",
#         "all_feasible": "Tất cả công thức đều khả thi 🎉",
#         "add_to_shopping": "Thêm nguyên liệu thiếu vào danh sách mua sắm",
#         "shopping_list": "🛒 Danh sách mua sắm",
#         "empty_list": "Danh sách mua sắm của bạn trống.",
#         "update_inventory": "Cập nhật kho từ danh sách mua sắm",
#         "purchased": "Kho đã được cập nhật với các mặt hàng đã mua.",
#         "select_recipes_label": "Chọn công thức để tiếp tục",
#         "select_purchased": "Chọn các mặt hàng đã mua",
#         "sent_to_shopping": "Nguyên liệu thiếu đã được thêm vào danh sách mua sắm.",
#         "cook_success": "Nấu thành công.",
#         "cook_failed": "Nấu thất bại: {error}",
#         "adjust_recipe": "⚖️ Điều chỉnh công thức",
#         "select_recipe": "Chọn công thức",
#         "adjustment_type": "Loại điều chỉnh",
#         "by_servings": "Theo khẩu phần",
#         "by_main_ingredient": "Theo nguyên liệu chính",
#         "new_servings": "Khẩu phần mới",
#         "main_ingredient": "Nguyên liệu chính",
#         "new_quantity": "Số lượng mới",
#         "spice_level": "Điều chỉnh độ cay",
#         "mild": "Nhẹ (60%)",
#         "normal": "Bình thường (80%)",
#         "rich": "Đậm (100%)",
#         "adjusted_recipe": "Công thức đã điều chỉnh",
#         "cook_adjusted": "Nấu công thức đã điều chỉnh",
#         "add_to_shopping_adjusted": "Thêm nguyên liệu thiếu vào danh sách mua sắm",
#         "adjusted_recipe_title": "Đã điều chỉnh: {title}",
#         "no_recipe_selected": "Vui lòng chọn một công thức để điều chỉnh.",
#         "invalid_adjustment": "Tham số điều chỉnh không hợp lệ.",
#         "cook_adjusted_success": "Công thức điều chỉnh '{title}' đã nấu thành công.",
#         "cook_adjusted_failed": "Không thể nấu công thức điều chỉnh '{title}': {error}",
#         "not_logged_in": "Bạn phải đăng nhập để truy cập trang này.",
#         "error_title_required": "Tiêu đề công thức là bắt buộc.",
#         "error_ingredients_required": "Cần ít nhất một nguyên liệu hợp lệ (với tên và số lượng dương).",
#         "duplicate_recipe": "Công thức với tiêu đề này đã tồn tại.",
#         "error_invalid_name": "Tên nguyên liệu không hợp lệ: {name}",
#         "error_invalid_unit": "Đơn vị không hợp lệ: {unit}",
#         "error_negative_qty": "Số lượng phải dương cho nguyên liệu: {name}",
#         "save_success": "Công thức '{title}' đã được lưu thành công.",
#         "update_success": "Công thức '{title}' đã được cập nhật thành công.",
#         "delete_success": "Công thức '{title}' đã được xóa thành công.",
#         "save_failed": "Không thể lưu công thức '{title}': {error}",
#         "update_failed": "Không thể cập nhật công thức '{title}': {error}",
#         "delete_failed": "Không thể xóa công thức '{title}'.",
#         "food_timeline": "🍲 Dòng thời gian món ăn",
#         "no_history": "Chưa có lịch sử nấu ăn.",
#         "no_entries": "Không có mục nào khớp với bộ lọc.",
#         "congrats": "Chúc mừng! Bạn đã đạt được {stars} với món {dish} 🎉",
#         "signature_dish": "Món tủ",
#         "search_placeholder": "Tìm kiếm (ví dụ: tag:signature, week:1, day:2025-09-01)",
#         "reset_filter": "🔄 Đặt lại bộ lọc",
#         "stats_week": "Tuần này bạn đã nấu {count} món, món thường xuyên nhất: {dish}",
#         "db_error": "Lỗi cơ sở dữ liệu: {error}",
#         "save_changes": "Save Changes",
#         "inventory_updated": "Inventory updated successfully.",
#         "db_init_failed": "Failed to initialize database: {error}",
#         "invalid_quantity": "Invalid quantity format. Use numbers with optional decimal point or comma."
#     }
# }

# # Database initialization
# def initialize_database() -> bool:
#     """Initialize PostgreSQL database and role if they don't exist."""
#     try:
#         conn = psycopg2.connect(
#             dbname="postgres",
#             user=POSTGRES_SUPERUSER,
#             password=POSTGRES_SUPERUSER_PASSWORD,
#             host="localhost",
#             port=5432
#         )
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (ROLE_NAME,))
#             if not cursor.fetchone():
#                 cursor.execute(f"CREATE ROLE {ROLE_NAME} WITH LOGIN PASSWORD %s", (ROLE_PASSWORD,))
#                 logger.info(f"Created PostgreSQL role: {ROLE_NAME}")
#             cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
#             if not cursor.fetchone():
#                 cursor.execute(f"CREATE DATABASE {DB_NAME}")
#                 cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {ROLE_NAME}")
#                 logger.info(f"Created PostgreSQL database: {DB_NAME}")
#         conn.close()
#         return True
#     except Exception as e:
#         logger.error(f"Failed to initialize database: {e}")
#         return False

# # Database setup
# try:
#     if not initialize_database():
#         st.error(get_text("db_init_failed").format(error="Could not initialize database. Check logs for details."))
#         st.stop()
#     engine = create_engine(DATABASE_URL, echo=False)
#     Base = declarative_base()
#     Session = scoped_session(sessionmaker(bind=engine))
# except Exception as e:
#     logger.error(f"Failed to connect to database: {e}")
#     st.error(get_text("db_error").format(error=str(e)))
#     st.stop()

# # Database Models
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     username = Column(String(255), unique=True, nullable=False)
#     password_hash = Column(String(128), nullable=False)
#     sec_question = Column(String(255), nullable=False)
#     sec_answer_hash = Column(String(128), nullable=False)
#     inventory = relationship("Inventory", back_populates="user")
#     recipes = relationship("Recipe", back_populates="user")
#     cooked_history = relationship("CookedHistory", back_populates="user")

# class Inventory(Base):
#     __tablename__ = "inventory"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     name = Column(String(255), nullable=False)
#     quantity = Column(Float, nullable=False)
#     unit = Column(String(50), nullable=False)
#     user = relationship("User", back_populates="inventory")

# class Recipe(Base):
#     __tablename__ = "recipes"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     title = Column(String(255), nullable=False)
#     category = Column(String(255))
#     instructions = Column(Text)
#     servings = Column(Float, default=1.0)
#     is_signature = Column(Boolean, default=False)
#     user = relationship("User", back_populates="recipes")
#     ingredients = relationship("RecipeIngredient", back_populates="recipe")

# class RecipeIngredient(Base):
#     __tablename__ = "recipe_ingredients"
#     id = Column(Integer, primary_key=True)
#     recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
#     name = Column(String(255), nullable=False)
#     quantity = Column(Float, nullable=False)
#     unit = Column(String(50), nullable=False)
#     is_spice = Column(Boolean, default=False)
#     recipe = relationship("Recipe", back_populates="ingredients")

# class CookedHistory(Base):
#     __tablename__ = "cooked_history"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
#     cooked_date = Column(DateTime, default=func.now())
#     user = relationship("User", back_populates="cooked_history")

# try:
#     Base.metadata.create_all(engine)
# except Exception as e:
#     logger.error(f"Failed to create tables: {e}")
#     st.error(get_text("db_error").format(error=str(e)))
#     st.stop()

# # Danh sách export
# __all__ = [
#     'inject_css', 'get_text', 'current_user_id', 'initialize_session_state',
#     'topbar_account', 'inventory_page', 'recipes_page', 'feasibility_page',
#     'shopping_list_page', 'recipe_adjustment_page', 'food_timeline_page',
#     'auth_gate_tabs', 'main'
# ]

# def inject_css() -> None:
#     """Inject custom CSS for Streamlit app styling."""
#     try:
#         st.markdown(
#             """
#             <style>
#                 .block-container {
#                     padding-top: 5rem;
#                     padding-bottom: 2rem;
#                     max-width: 980px;
#                 }
#                 .stTextInput > div > div > input,
#                 .stNumberInput > div > div > input,
#                 textarea {
#                     border-radius: 12px !important;
#                     border: 1px solid #e6e6e6 !important;
#                     padding: .55rem .8rem !important;
#                 }
#                 .stButton > button {
#                     background: #111 !important;
#                     color: #fff !important;
#                     border: none !important;
#                     border-radius: 14px !important;
#                     padding: .55rem 1rem !important;
#                     font-weight: 500 !important;
#                     transition: transform .12s ease, opacity .12s ease;
#                 }
#                 .stButton > button:hover {
#                     transform: translateY(-1px);
#                     opacity: .95;
#                 }
#                 table {
#                     border-collapse: collapse;
#                     width: 100%;
#                 }
#                 th, td {
#                     padding: 8px 10px;
#                     border-bottom: 1px solid #eee;
#                 }
#                 th {
#                     color: #666;
#                     font-weight: 600;
#                 }
#                 td {
#                     color: #222;
#                 }
#                 .stTabs [data-baseweb="tab-list"] {
#                     gap: .25rem;
#                     margin-top: 1rem;
#                 }
#                 .stTabs [data-baseweb="tab"] {
#                     padding: .6rem 1rem;
#                 }
#                 .streamlit-expanderHeader {
#                     font-weight: 600;
#                 }
#                 #topbar-account {
#                     margin-bottom: 1rem;
#                 }
#                 .food-card {
#                     border: 1px solid #eee;
#                     border-radius: 12px;
#                     padding: 1rem;
#                     margin-bottom: 1rem;
#                     background-color: #f9f9f9;
#                 }
#                 .dish-name {
#                     font-weight: bold;
#                     font-size: 1.2em;
#                 }
#                 .stars {
#                     font-size: 1.2em;
#                     color: #FFD700;
#                     text-align: right;
#                 }
#                 @media (max-width: 600px) {
#                     .block-container {
#                         padding-top: 4rem;
#                         padding-left: 1rem;
#                         padding-right: 1rem;
#                     }
#                     .stButton > button {
#                         width: 100%;
#                         margin-bottom: 0.5rem;
#                     }
#                     .stTabs [data-baseweb="tab-list"] {
#                         margin-top: 0.5rem;
#                     }
#                 }
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )
#     except Exception as e:
#         logger.error(f"Error injecting CSS: {e}")
#         st.error("Cannot apply custom styling. Continuing with default.")

# def get_text(key: str, **kwargs) -> str:
#     """Retrieve multilingual text with safe formatting."""
#     lang = st.session_state.get("language", "English")
#     template = TEXT.get(lang, TEXT["English"]).get(key, key)
#     if kwargs:
#         try:
#             return template.format(**kwargs)
#         except Exception as e:
#             logger.warning(f"i18n fallback for key='{key}': {e}")
#             return template
#     return template

# def current_user_id() -> Optional[int]:
#     """Get current user ID from session state."""
#     return st.session_state.get("user_id")

# def initialize_session_state() -> None:
#     """Initialize session state with default values."""
#     defaults = {
#         "user_id": None,
#         "username": None,
#         "language": "English",
#         "editing_recipe_id": None,
#         "recipe_form_data": {
#             "title": "",
#             "category": "",
#             "instructions": "",
#             "is_signature": False,
#             "servings": 1.0,
#             "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#         },
#         "shopping_list_data": [],
#         "adjusted_recipe": None,
#         "search_value": ""
#     }
#     for key, value in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = value

# def topbar_account() -> None:
#     """Display top bar with username, language selector, and logout button."""
#     user_id = current_user_id()
#     if not user_id:
#         return
#     with st.container():
#         st.markdown('<div id="topbar-account">', unsafe_allow_html=True)
#         col1, col2, col3 = st.columns([3, 1, 1])
#         with col1:
#             st.write(f"{get_text('username')}: {html.escape(st.session_state.get('username', 'Unknown'))}")
#         with col2:
#             st.selectbox(
#                 get_text("language"),
#                 ["English", "Vietnamese"],
#                 index=0 if st.session_state.get("language", "English") == "English" else 1,
#                 key="language_selector",
#                 on_change=lambda: st.session_state.update({"language": st.session_state.language_selector})
#             )
#         with col3:
#             if st.button(get_text("logout"), key="logout_button"):
#                 st.session_state.clear()
#                 initialize_session_state()
#                 logger.info(f"User {st.session_state.get('username', 'Unknown')} logged out")
#                 st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)

# def calculate_stars(count: int, is_signature: bool) -> int:
#     """Calculate stars based on cook count and signature status."""
#     if not isinstance(count, int) or count < 0:
#         return 0
#     thresholds = [(15, 5), (8, 4), (5, 3), (3, 2), (1, 1)]
#     return 5 if is_signature else next((stars for threshold, stars in thresholds if count >= threshold), 0)

# def _norm_name(name: str) -> str:
#     """Normalize ingredient name for comparison."""
#     return (name or "").strip().lower()

# def _norm_unit(unit: str) -> str:
#     """Normalize unit for comparison."""
#     return (unit or "").strip().lower()

# def _inventory_map(user_id: int) -> Dict[Tuple[str, str], dict]:
#     """Create inventory map based on normalized name and unit."""
#     with Session() as session:
#         try:
#             items = session.query(Inventory).filter_by(user_id=user_id).all()
#             return {
#                 (_norm_name(item.name), _norm_unit(item.unit)): {
#                     "id": item.id,
#                     "name": item.name,
#                     "quantity": item.quantity,
#                     "unit": item.unit
#                 }
#                 for item in items if item.name and item.unit
#             }
#         except SQLAlchemyError as e:
#             logger.error(f"Error fetching inventory map for user {user_id}: {e}")
#             raise

# def validate_ingredients(recipe: Dict, inventory_map: Dict[Tuple[str, str], dict]) -> Tuple[bool, Optional[str]]:
#     """Validate recipe ingredients and check feasibility against inventory."""
#     if not recipe.get("ingredients"):
#         return False, get_text("error_ingredients_required")
    
#     for ing in recipe.get("ingredients", []):
#         name = _norm_name(ing.get("name", ""))
#         unit = _norm_unit(ing.get("unit", ""))
#         qty = float(ing.get("quantity", 0.0))
        
#         if not name or qty <= 0:
#             return False, get_text("error_ingredients_required")
#         if not DatabaseManager.validate_name(ing.get("name", "")):
#             return False, get_text("error_invalid_name").format(name=ing.get("name"))
#         if unit not in [_norm_unit(u) for u in VALID_UNITS]:
#             return False, get_text("error_invalid_unit").format(unit=ing.get("unit"))
        
#         key = (name, unit)
#         inv_item = inventory_map.get(key)
#         if not inv_item:
#             return False, f"Ingredient {ing.get('name')} not found in inventory"
#         if inv_item["unit"] != ing.get("unit"):
#             return False, f"Unit mismatch for {ing.get('name')}: expected {ing.get('unit')}, found {inv_item['unit']}"
#         if inv_item["quantity"] < qty:
#             return False, f"Insufficient quantity for {ing.get('name')}: need {qty}, have {inv_item['quantity']}"
    
#     return True, None

# def recipe_feasibility(recipe: Dict, user_id: int) -> Tuple[bool, List[Dict]]:
#     """Check recipe feasibility based on inventory."""
#     try:
#         inv_map = _inventory_map(user_id)
#         shorts = []
#         feasible = True
        
#         for ing in recipe.get("ingredients", []):
#             name = _norm_name(ing.get("name", ""))
#             unit = _norm_unit(ing.get("unit", ""))
#             qty = float(ing.get("quantity", 0.0))
#             key = (name, unit)
#             inv_item = inv_map.get(key, {})
#             have_qty = float(inv_item.get("quantity", 0.0))
#             missing = max(0.0, qty - have_qty)
            
#             if missing > 1e-9 or not inv_item:
#                 feasible = False
#                 shorts.append({
#                     "name": ing.get("name", ""),
#                     "needed_qty": qty,
#                     "have_qty": have_qty,
#                     "needed_unit": ing.get("unit", ""),
#                     "have_unit": inv_item.get("unit", "") if inv_item else "",
#                     "missing_qty_disp": missing,
#                     "missing_unit_disp": ing.get("unit", "")
#                 })
        
#         return feasible, shorts
#     except SQLAlchemyError as e:
#         logger.error(f"Error checking recipe feasibility: {e}")
#         raise

# def consume_ingredients_for_recipe(recipe: Dict, user_id: int) -> Tuple[bool, str]:
#     """Consume ingredients from inventory if recipe is feasible."""
#     with Session() as session:
#         try:
#             inv_map = _inventory_map(user_id)
#             is_valid, error = validate_ingredients(recipe, inv_map)
#             if not is_valid:
#                 logger.warning(f"Validation failed for recipe {recipe.get('title', 'Unknown')}: {error}")
#                 return False, get_text("cook_failed").format(error=error)
            
#             for ing in recipe.get("ingredients", []):
#                 name = _norm_name(ing.get("name", ""))
#                 unit = _norm_unit(ing.get("unit", ""))
#                 qty = float(ing.get("quantity", 0.0))
#                 key = (name, unit)
#                 inv_item = inv_map.get(key)
                
#                 if not inv_item:
#                     raise ValueError(f"Ingredient {ing.get('name')} not found in inventory")
#                 if inv_item["unit"] != ing.get("unit"):
#                     raise ValueError(f"Unit mismatch for {ing.get('name')}")
#                 if inv_item["quantity"] < qty:
#                     raise ValueError(f"Insufficient quantity for {ing.get('name')}")
                
#                 inventory_item = session.query(Inventory).filter_by(id=inv_item["id"]).first()
#                 inventory_item.quantity = max(0.0, inventory_item.quantity - qty)
            
#             session.commit()
#             logger.info(f"Successfully consumed ingredients for recipe {recipe.get('title', 'Unknown')}")
#             return True, get_text("cook_success")
#         except Exception as e:
#             session.rollback()
#             logger.error(f"Failed to consume ingredients for recipe {recipe.get('title', 'Unknown')}: {str(e)}")
#             return False, get_text("cook_failed").format(error=str(e))

# def normalize_quantity(quantity: Any) -> float:
#     """Normalize quantity input to float, handling strings with commas or decimals."""
#     if isinstance(quantity, (int, float)):
#         return float(quantity)
#     if isinstance(quantity, str):
#         try:
#             return float(quantity.replace(',', '.').strip())
#         except ValueError:
#             raise ValueError(get_text("invalid_quantity"))
#     raise ValueError(get_text("invalid_quantity"))

# class DatabaseManager:
#     @staticmethod
#     def validate_name(name: str) -> bool:
#         """Validate ingredient or user name, allowing Unicode characters."""
#         return bool(name and name.strip() and all(c.isprintable() for c in name))

#     @staticmethod
#     def normalize_name(name: str) -> str:
#         """Normalize name for comparison."""
#         return _norm_name(name)

#     @classmethod
#     def verify_login(cls, username: str, password: str) -> Optional[int]:
#         """Verify user login credentials."""
#         if not username or not password or len(password) < 8:
#             return None
#         with Session() as session:
#             try:
#                 user = session.query(User).filter_by(username=username).first()
#                 if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
#                     return user.id
#                 return None
#             except SQLAlchemyError as e:
#                 logger.error(f"Error verifying login for {username}: {e}")
#                 raise

#     @classmethod
#     def create_user(cls, username: str, password: str, sec_question: str, sec_answer: str) -> Tuple[bool, str]:
#         """Create a new user."""
#         if not all([username.strip(), password.strip(), sec_question.strip(), sec_answer.strip()]):
#             return False, "All fields required."
#         if len(password) < 8:
#             return False, "Password must be at least 8 characters."
#         if not cls.validate_name(username):
#             return False, get_text("error_invalid_name").format(name=username)
        
#         with Session() as session:
#             try:
#                 if session.query(User).filter_by(username=username).first():
#                     return False, "Username already exists."
#                 password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 sec_answer_hash = bcrypt.hashpw(sec_answer.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 user = User(
#                     username=username,
#                     password_hash=password_hash,
#                     sec_question=sec_question,
#                     sec_answer_hash=sec_answer_hash
#                 )
#                 session.add(user)
#                 session.commit()
#                 logger.info(f"Created user: {username}")
#                 return True, "User created successfully."
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error creating user {username}: {e}")
#                 return False, get_text("db_error").format(error=str(e))

#     @classmethod
#     def reset_password(cls, username: str, sec_answer: str, new_password: str) -> bool:
#         """Reset user password."""
#         if not all([username.strip(), sec_answer.strip(), new_password.strip()]):
#             return False
#         if len(new_password) < 8:
#             return False
#         with Session() as session:
#             try:
#                 user = session.query(User).filter_by(username=username).first()
#                 if not user:
#                     return False
#                 if bcrypt.checkpw(sec_answer.encode('utf-8'), user.sec_answer_hash.encode('utf-8')):
#                     user.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                     session.commit()
#                     logger.info(f"Password reset for user: {username}")
#                     return True
#                 return False
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error resetting password for {username}: {e}")
#                 return False

#     @classmethod
#     def list_inventory(cls, user_id: int) -> List[Dict]:
#         """List user inventory."""
#         with Session() as session:
#             try:
#                 items = session.query(Inventory).filter_by(user_id=user_id).all()
#                 return [
#                     {"id": item.id, "name": item.name, "quantity": item.quantity, "unit": item.unit}
#                     for item in items
#                 ]
#             except SQLAlchemyError as e:
#                 logger.error(f"Error listing inventory for user {user_id}: {e}")
#                 raise

#     @classmethod
#     def upsert_inventory(cls, user_id: int, name: str, quantity: float, unit: str) -> bool:
#         """Add or update inventory item."""
#         with Session() as session:
#             try:
#                 if not cls.validate_name(name):
#                     logger.error(f"Invalid name for inventory item: {name}")
#                     return False
#                 if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                     logger.error(f"Invalid unit for inventory item: {unit}")
#                     return False
#                 if quantity < 0:
#                     logger.error(f"Negative quantity for inventory item: {name}")
#                     return False
#                 item = session.query(Inventory).filter_by(
#                     user_id=user_id,
#                     name=cls.normalize_name(name),
#                     unit=_norm_unit(unit)
#                 ).first()
#                 if item:
#                     item.quantity = max(0.0, item.quantity + quantity)
#                 else:
#                     item = Inventory(
#                         user_id=user_id,
#                         name=name,
#                         quantity=max(0.0, quantity),
#                         unit=unit
#                     )
#                     session.add(item)
#                 session.commit()
#                 logger.info(f"Upserted inventory item: {name} for user {user_id}")
#                 return True
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error upserting inventory for user {user_id}: {e}")
#                 return False

#     @classmethod
#     def update_inventory_item(cls, user_id: int, item_id: int, name: str, quantity: float, unit: str) -> Tuple[bool, str]:
#         """Update specific inventory item by ID."""
#         with Session() as session:
#             try:
#                 item = session.query(Inventory).filter_by(id=item_id, user_id=user_id).first()
#                 if not item:
#                     logger.error(f"Inventory item not found: id={item_id}, user_id={user_id}")
#                     return False, "Item not found."
#                 if not cls.validate_name(name):
#                     logger.error(f"Invalid name for inventory item: {name}")
#                     return False, get_text("error_invalid_name").format(name=name)
#                 if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                     logger.error(f"Invalid unit for inventory item: {unit}")
#                     return False, get_text("error_invalid_unit").format(unit=unit)
#                 if quantity < 0:
#                     logger.error(f"Negative quantity for inventory item: {name}")
#                     return False, get_text("error_negative_qty").format(name=name)
#                 item.name = name
#                 item.quantity = max(0.0, quantity)
#                 item.unit = unit
#                 session.commit()
#                 logger.info(f"Updated inventory item: id={item_id} for user {user_id}")
#                 return True, "Inventory item updated successfully."
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error updating inventory item {item_id}: {e}")
#                 return False, get_text("db_error").format(error=str(e))

#     @classmethod
#     def delete_inventory(cls, user_id: int, item_id: int) -> bool:
#         """Delete inventory item by ID."""
#         with Session() as session:
#             try:
#                 item = session.query(Inventory).filter_by(id=item_id, user_id=user_id).first()
#                 if item:
#                     session.delete(item)
#                     session.commit()
#                     logger.info(f"Deleted inventory item: id={item_id} for user {user_id}")
#                     return True
#                 return False
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error deleting inventory item {item_id}: {e}")
#                 return False

#     @classmethod
#     def list_recipes(cls, user_id: int) -> List[Dict]:
#         """List user recipes."""
#         with Session() as session:
#             try:
#                 recipes = session.query(Recipe).filter_by(user_id=user_id).all()
#                 return [
#                     {
#                         "id": r.id,
#                         "title": r.title,
#                         "category": r.category,
#                         "instructions": r.instructions,
#                         "servings": r.servings,
#                         "is_signature": r.is_signature,
#                         "ingredients": [
#                             {
#                                 "name": i.name,
#                                 "quantity": i.quantity,
#                                 "unit": i.unit,
#                                 "is_spice": i.is_spice
#                             } for i in r.ingredients
#                         ]
#                     } for r in recipes
#                 ]
#             except SQLAlchemyError as e:
#                 logger.error(f"Error listing recipes for user {user_id}: {e}")
#                 raise

#     @classmethod
#     def create_recipe(cls, user_id: int, title: str, category: str, instructions: str, 
#                      ingredients: List[Dict], recipe_id: Optional[int] = None, is_signature: bool = False) -> Tuple[bool, str]:
#         """Create or update a recipe."""
#         with Session() as session:
#             try:
#                 if not title.strip():
#                     return False, get_text("error_title_required")
#                 if not any(ing["name"].strip() and ing["quantity"] > 0 for ing in ingredients):
#                     return False, get_text("error_ingredients_required")
                
#                 if session.query(Recipe).filter_by(user_id=user_id, title=title).filter(Recipe.id != recipe_id).first():
#                     return False, get_text("duplicate_recipe")
                
#                 if recipe_id:
#                     recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
#                     if not recipe:
#                         return False, get_text("delete_failed").format(title=title)
#                     recipe.title = title
#                     recipe.category = category
#                     recipe.instructions = instructions
#                     recipe.is_signature = is_signature
#                     recipe.servings = 1.0
#                     session.query(RecipeIngredient).filter_by(recipe_id=recipe_id).delete()
#                 else:
#                     recipe = Recipe(
#                         user_id=user_id,
#                         title=title,
#                         category=category,
#                         instructions=instructions,
#                         servings=1.0,
#                         is_signature=is_signature
#                     )
#                     session.add(recipe)
#                     session.flush()
                
#                 for ing in ingredients:
#                     if not cls.validate_name(ing["name"]):
#                         return False, get_text("error_invalid_name").format(name=ing["name"])
#                     if _norm_unit(ing["unit"]) not in [_norm_unit(u) for u in VALID_UNITS]:
#                         return False, get_text("error_invalid_unit").format(unit=ing["unit"])
#                     if ing["quantity"] <= 0:
#                         return False, get_text("error_negative_qty").format(name=ing["name"])
#                     session.add(RecipeIngredient(
#                         recipe_id=recipe.id,
#                         name=ing["name"],
#                         quantity=ing["quantity"],
#                         unit=ing["unit"],
#                         is_spice=ing.get("is_spice", False)
#                     ))
                
#                 session.commit()
#                 logger.info(f"{'Updated' if recipe_id else 'Created'} recipe: {title} for user {user_id}")
#                 return True, get_text("update_success" if recipe_id else "save_success").format(title=title)
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error saving recipe {title}: {e}")
#                 return False, get_text("save_failed").format(title=title, error=str(e))

#     @classmethod
#     def delete_recipe(cls, user_id: int, recipe_id: int) -> bool:
#         """Delete a recipe."""
#         with Session() as session:
#             try:
#                 recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
#                 if recipe:
#                     session.delete(recipe)
#                     session.commit()
#                     logger.info(f"Deleted recipe: id={recipe_id} for user {user_id}")
#                     return True
#                 return False
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error deleting recipe {recipe_id}: {e}")
#                 return False

#     @classmethod
#     def log_cooked_recipe(cls, user_id: int, recipe_id: int) -> bool:
#         """Log a cooked recipe."""
#         with Session() as session:
#             try:
#                 session.add(CookedHistory(user_id=user_id, recipe_id=recipe_id))
#                 session.commit()
#                 logger.info(f"Logged cooked recipe: id={recipe_id} for user {user_id}")
#                 return True
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error logging cooked recipe {recipe_id}: {e}")
#                 return False

#     @classmethod
#     def list_cooked_history(cls, user_id: int) -> List[Dict]:
#         """List cooking history."""
#         with Session() as session:
#             try:
#                 history = session.query(CookedHistory).filter_by(user_id=user_id).all()
#                 return [
#                     {"recipe_id": h.recipe_id, "cooked_date": h.cooked_date.strftime("%Y-%m-%d %H:%M:%S")}
#                     for h in history
#                 ]
#             except SQLAlchemyError as e:
#                 logger.error(f"Error listing cooked history for user {user_id}: {e}")
#                 raise

#     @classmethod
#     def get_cooked_count(cls, user_id: int, recipe_id: int) -> int:
#         """Get count of times a recipe was cooked."""
#         with Session() as session:
#             try:
#                 return session.query(CookedHistory).filter_by(user_id=user_id, recipe_id=recipe_id).count()
#             except SQLAlchemyError as e:
#                 logger.error(f"Error getting cooked count for recipe {recipe_id}: {e}")
#                 raise

# def inventory_page() -> None:
#     """Display and manage ingredient inventory."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading inventory for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     st.header(get_text("inventory"))
#     st.subheader(get_text("your_stock"))
#     st.caption(get_text("unit_tips"))

#     with st.expander(get_text("add_ingredient")):
#         with st.form(key="add_inventory_form"):
#             col1, col2, col3 = st.columns([2, 1, 1])
#             with col1:
#                 ingredient_name = st.text_input(get_text("name"), placeholder=get_text("e.g., chicken"), key="new_ingredient_name")
#             with col2:
#                 quantity_input = st.text_input(get_text("quantity"), value="0.0", key="new_quantity")
#             with col3:
#                 unit = st.selectbox(get_text("unit"), options=VALID_UNITS, key="new_unit")
#             if st.form_submit_button(get_text("add_ingredient")):
#                 try:
#                     quantity = normalize_quantity(quantity_input)
#                     if not ingredient_name.strip():
#                         st.error(get_text("error_ingredients_required"))
#                     elif not DatabaseManager.validate_name(ingredient_name):
#                         st.error(get_text("error_invalid_name").format(name=ingredient_name))
#                     elif _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                         st.error(get_text("error_invalid_unit").format(unit=unit))
#                     elif quantity < 0:
#                         st.error(get_text("error_negative_qty").format(name=ingredient_name))
#                     else:
#                         if DatabaseManager.upsert_inventory(user_id, ingredient_name.strip(), quantity, unit):
#                             st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                             st.success(get_text("save_success").format(title=ingredient_name))
#                             st.rerun()
#                         else:
#                             st.error(get_text("save_failed").format(title=ingredient_name, error="Could not add ingredient"))
#                 except ValueError as e:
#                     st.error(str(e))
#                 except SQLAlchemyError as e:
#                     logger.error(f"Error adding ingredient {ingredient_name}: {e}")
#                     st.error(get_text("db_error").format(error=str(e)))

#     edited_data = st.data_editor(
#         inventory,
#         column_config={
#             "id": None,
#             "name": st.column_config.TextColumn(get_text("name"), required=True),
#             "quantity": st.column_config.NumberColumn(
#                 get_text("quantity"),
#                 min_value=0.0,
#                 format="%.2f",
#                 required=True
#             ),
#             "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#         },
#         num_rows="dynamic",
#         key=f"inventory_editor_{user_id}",
#         hide_index=True
#     )

#     if st.button(get_text("save_changes"), key="save_inventory_changes"):
#         errors = []
#         validated_data = []
#         for item in edited_data:
#             name = item.get("name", "").strip()
#             unit = item.get("unit", "")
#             quantity = item.get("quantity")
#             if not name or quantity is None or not unit:
#                 errors.append(get_text("error_ingredients_required"))
#                 continue
#             if not DatabaseManager.validate_name(name):
#                 errors.append(get_text("error_invalid_name").format(name=name))
#                 continue
#             if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                 errors.append(get_text("error_invalid_unit").format(unit=unit))
#                 continue
#             if quantity < 0:
#                 errors.append(get_text("error_negative_qty").format(name=name))
#                 continue
#             validated_data.append({"id": item.get("id"), "name": name, "quantity": float(quantity), "unit": unit})

#         if errors:
#             for error in errors:
#                 st.error(error)
#         else:
#             try:
#                 old_ids = {item.get("id") for item in inventory if item.get("id")}
#                 edited_ids = {item.get("id") for item in validated_data if item.get("id")}
#                 deleted_ids = old_ids - edited_ids
#                 for item_id in deleted_ids:
#                     if DatabaseManager.delete_inventory(user_id, item_id):
#                         logger.info(f"Deleted inventory item: id={item_id} for user {user_id}")
#                 for item in validated_data:
#                     if item.get("id"):
#                         success, message = DatabaseManager.update_inventory_item(user_id, item["id"], item["name"], item["quantity"], item["unit"])
#                         if not success:
#                             st.error(message)
#                             continue
#                     else:
#                         if not DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"]):
#                             st.error(get_text("save_failed").format(title=item["name"], error="Could not add ingredient"))
#                             continue
#                 st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                 st.success(get_text("inventory_updated"))
#                 st.rerun()
#             except SQLAlchemyError as e:
#                 logger.error(f"Error updating inventory: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

#     if not inventory:
#         st.info(get_text("no_ingredients"))

# def recipes_page() -> None:
#     """Display and manage user recipes."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading recipes for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     st.header(get_text("recipes"))
#     st.subheader(get_text("your_recipes"))
#     st.caption(get_text("unit_tips"))

#     if not recipes:
#         st.info(get_text("no_recipes"))

#     form_data = st.session_state.recipe_form_data
#     recipe_id = st.session_state.get("editing_recipe_id")

#     with st.form(key="recipe_form"):
#         title = st.text_input(get_text("title"), value=form_data["title"], key="recipe_title")
#         category = st.text_input(get_text("category"), value=form_data["category"], key="recipe_category")
#         instructions = st.text_area(get_text("instructions"), value=form_data["instructions"], key="recipe_instructions")
#         is_signature = st.checkbox(get_text("signature_dish"), value=form_data["is_signature"], key="recipe_is_signature")
#         ingredients_data = st.data_editor(
#             form_data["ingredients"],
#             column_config={
#                 "name": st.column_config.TextColumn(get_text("name"), required=True),
#                 "quantity": st.column_config.NumberColumn(
#                     get_text("quantity"),
#                     min_value=0.0,
#                     format="%.2f",
#                     required=True
#                 ),
#                 "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#                 "is_spice": st.column_config.CheckboxColumn("Spice", default=False)
#             },
#             num_rows="dynamic",
#             key="ingredients_editor",
#             hide_index=True
#         )

#         submit_label = get_text("update_recipe") if recipe_id else get_text("save_recipe")
#         if st.form_submit_button(submit_label):
#             if not title.strip():
#                 st.error(get_text("error_title_required"))
#                 return
#             valid_ingredients = []
#             for ing in ingredients_data:
#                 name = ing.get("name", "").strip()
#                 quantity = ing.get("quantity")
#                 unit = ing.get("unit", "")
#                 is_spice = ing.get("is_spice", False)
#                 if not name or quantity is None or not unit:
#                     st.error(get_text("error_ingredients_required"))
#                     return
#                 if not DatabaseManager.validate_name(name):
#                     st.error(get_text("error_invalid_name").format(name=name))
#                     return
#                 if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#                     st.error(get_text("error_invalid_unit").format(unit=unit))
#                     return
#                 if quantity <= 0:
#                     st.error(get_text("error_negative_qty").format(name=name))
#                     return
#                 valid_ingredients.append({
#                     "name": name,
#                     "quantity": float(quantity),
#                     "unit": unit,
#                     "is_spice": is_spice
#                 })
#             if not valid_ingredients:
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             existing_recipe = next((r for r in recipes if r.get("title") == title.strip() and r.get("id") != recipe_id), None)
#             if existing_recipe:
#                 st.error(get_text("duplicate_recipe"))
#                 return
#             try:
#                 success, message = DatabaseManager.create_recipe(
#                     user_id, title.strip(), category.strip(), instructions.strip(), 
#                     valid_ingredients, recipe_id, is_signature
#                 )
#                 if success:
#                     st.success(message)
#                     st.session_state.recipe_form_data = {
#                         "title": "",
#                         "category": "",
#                         "instructions": "",
#                         "is_signature": False,
#                         "servings": 1.0,
#                         "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}]
#                     }
#                     st.session_state.editing_recipe_id = None
#                     st.rerun()
#                 else:
#                     st.error(message)
#             except SQLAlchemyError as e:
#                 logger.error(f"Error saving recipe {title}: {e}")
#                 st.error(get_text("save_failed").format(title=title, error=str(e)))

#     if recipes:
#         for recipe in recipes:
#             signature_text = f" - {get_text('signature_dish')}" if recipe.get("is_signature") else ""
#             with st.expander(f"{html.escape(recipe.get('title', 'Untitled'))} ({html.escape(recipe.get('category', '-'))}) {signature_text}"):
#                 st.write(f"**{get_text('instructions')}:** {html.escape(recipe.get('instructions', ''))}")
#                 st.table([
#                     {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
#                      get_text("unit"): ing["unit"], "Spice": "Yes" if ing.get("is_spice") else "No"}
#                     for ing in recipe.get("ingredients", [])
#                 ])
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button(get_text("update_recipe"), key=f"edit_{recipe.get('id')}"):
#                         st.session_state.editing_recipe_id = recipe["id"]
#                         st.session_state.recipe_form_data = {
#                             "title": recipe["title"],
#                             "category": recipe["category"],
#                             "instructions": recipe["instructions"],
#                             "is_signature": recipe.get("is_signature", False),
#                             "servings": recipe.get("servings", 1.0),
#                             "ingredients": [
#                                 {"name": ing["name"], "quantity": ing["quantity"], "unit": ing["unit"], "is_spice": ing.get("is_spice", False)}
#                                 for ing in recipe.get("ingredients", [])
#                             ]
#                         }
#                         st.rerun()
#                 with col2:
#                     if st.button(get_text("delete_recipe"), key=f"delete_{recipe.get('id')}"):
#                         try:
#                             if DatabaseManager.delete_recipe(user_id, recipe["id"]):
#                                 st.success(get_text("delete_success").format(title=recipe["title"]))
#                                 st.rerun()
#                             else:
#                                 st.error(get_text("delete_failed").format(title=recipe["title"]))
#                         except SQLAlchemyError as e:
#                             logger.error(f"Error deleting recipe {recipe['title']}: {e}")
#                             st.error(get_text("delete_failed").format(title=recipe["title"]))

# def feasibility_page() -> None:
#     """Display recipe feasibility and shopping list options."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading data for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     if not recipes:
#         st.info(get_text("create_recipes_first"))
#         return

#     st.header(get_text("feasibility"))
#     st.subheader(get_text("you_can_cook"))

#     recipe_results = [
#         {"recipe": r, "feasible": feasible, "shorts": shorts}
#         for r in recipes
#         for feasible, shorts in [recipe_feasibility(r, user_id)]
#     ]

#     if not recipe_results:
#         st.info(get_text("none_yet"))
#         return

#     if all(r["feasible"] for r in recipe_results):
#         st.success(get_text("all_feasible"))

#     selected_titles = st.multiselect(
#         get_text("select_recipes_label"),
#         [r["recipe"]["title"] for r in recipe_results],
#         format_func=lambda t: f"{t} {'✅' if next((r for r in recipe_results if r['recipe']['title'] == t), {}).get('feasible', False) else '❌'}",
#         key="select_recipes_feasibility"
#     )

#     selected_missing = []
#     for result in [r for r in recipe_results if r["recipe"]["title"] in selected_titles]:
#         st.markdown(f"#### {html.escape(result['recipe'].get('title', 'Untitled'))}")
#         if result["feasible"]:
#             st.success(get_text("all_available"))
#             if st.button(get_text("cook"), key=f"cook_{result['recipe'].get('id')}"):
#                 try:
#                     success, message = consume_ingredients_for_recipe(result["recipe"], user_id)
#                     if success:
#                         DatabaseManager.log_cooked_recipe(user_id, result["recipe"]["id"])
#                         count = DatabaseManager.get_cooked_count(user_id, result["recipe"]["id"])
#                         stars = calculate_stars(count, result["recipe"].get("is_signature", False))
#                         if stars > calculate_stars(count - 1, result["recipe"].get("is_signature", False)):
#                             st.success(get_text("congrats").format(stars="⭐" * stars, dish=result["recipe"]["title"]))
#                         st.success(message)
#                         st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                         st.rerun()
#                     else:
#                         st.error(message)
#                         _, shorts = recipe_feasibility(result["recipe"], user_id)
#                         if shorts:
#                             st.table([
#                                 {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
#                                  get_text("have"): f"{s['have_qty']} {s['have_unit']}",
#                                  get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
#                                 for s in shorts
#                             ])
#                 except SQLAlchemyError as e:
#                     logger.error(f"Error cooking recipe {result['recipe']['title']}: {e}")
#                     st.error(get_text("db_error").format(error=str(e)))
#         else:
#             st.warning(get_text("missing_something"))
#             st.table([
#                 {get_text("name"): s["name"], get_text("need"): s["needed_qty"], get_text("have"): s["have_qty"],
#                  get_text("unit"): s["needed_unit"], get_text("missing"): s["missing_qty_disp"]}
#                 for s in result["shorts"]
#             ])
#             selected_missing.extend(result["shorts"])

#     if selected_missing and st.button(get_text("add_to_shopping"), key="add_to_shopping_feasibility"):
#         try:
#             agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
#             for s in selected_missing:
#                 key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
#                 agg_missing[key]["name"] = s["name"]
#                 agg_missing[key]["quantity"] += s["missing_qty_disp"]
#                 agg_missing[key]["unit"] = s["missing_unit_disp"]
#             st.session_state["shopping_list_data"] = list(agg_missing.values())
#             st.success(get_text("sent_to_shopping"))
#             st.rerun()
#         except SQLAlchemyError as e:
#             logger.error(f"Error adding to shopping list: {e}")
#             st.error(get_text("db_error").format(error=str(e)))

# def shopping_list_page() -> None:
#     """Manage shopping list and update inventory."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading inventory for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     shopping_list = st.session_state.get("shopping_list_data", [])
#     st.header(get_text("shopping_list"))
#     if not shopping_list:
#         st.info(get_text("empty_list"))
#         return

#     valid_shopping_list = []
#     for item in shopping_list:
#         try:
#             quantity = normalize_quantity(item.get("quantity", 0.0))
#             if (isinstance(item, dict) and
#                     item.get("name") and isinstance(item.get("name"), str) and
#                     quantity >= 0 and
#                     item.get("unit") and _norm_unit(item["unit"]) in [_norm_unit(u) for u in VALID_UNITS]):
#                 valid_shopping_list.append({
#                     "name": item["name"],
#                     "quantity": quantity,
#                     "unit": item["unit"]
#                 })
#             else:
#                 logger.warning(f"Invalid shopping list item: {item}")
#         except ValueError as e:
#             logger.warning(f"Invalid quantity in shopping list item: {item}, error: {e}")
#     shopping_list = valid_shopping_list
#     st.session_state["shopping_list_data"] = shopping_list

#     shopping_data = st.data_editor(
#         shopping_list,
#         column_config={
#             "name": st.column_config.TextColumn(get_text("name"), required=True),
#             "quantity": st.column_config.NumberColumn(
#                 get_text("quantity"),
#                 min_value=0.0,
#                 format="%.2f",
#                 required=True
#             ),
#             "unit": st.column_config.SelectboxColumn(get_text("unit"), options=VALID_UNITS, required=True),
#         },
#         num_rows="dynamic",
#         key="shopping_list_editor",
#         hide_index=True
#     )

#     validated_shopping_data = []
#     for item in shopping_data:
#         name = item.get("name", "").strip()
#         quantity = item.get("quantity")
#         unit = item.get("unit", "")
#         if not name or quantity is None or not unit:
#             st.error(get_text("error_ingredients_required"))
#             return
#         if not DatabaseManager.validate_name(name):
#             st.error(get_text("error_invalid_name").format(name=name))
#             return
#         if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
#             st.error(get_text("error_invalid_unit").format(unit=unit))
#             return
#         if quantity < 0:
#             st.error(get_text("error_negative_qty").format(name=name))
#             return
#         validated_shopping_data.append({
#             "name": name,
#             "quantity": float(quantity),
#             "unit": unit
#         })
#     st.session_state["shopping_list_data"] = validated_shopping_data

#     purchased_labels = [f"{item['name']} ({item['unit']})" for item in validated_shopping_data if item.get("name") and item.get("unit")]
#     purchased_names = st.multiselect(get_text("select_purchased"), options=purchased_labels, key="select_purchased_shopping")

#     if st.button(get_text("update_inventory"), key="update_inventory_shopping"):
#         with Session() as session:
#             try:
#                 for item in validated_shopping_data:
#                     item_label = f"{item['name']} ({item['unit']})"
#                     if item_label in purchased_names:
#                         if not DatabaseManager.upsert_inventory(user_id, item["name"], item["quantity"], item["unit"]):
#                             st.error(get_text("save_failed").format(title=item["name"], error="Could not update inventory"))
#                             continue
#                 st.session_state["shopping_list_data"] = [
#                     item for item in validated_shopping_data if f"{item['name']} ({item['unit']})" not in purchased_names
#                 ]
#                 session.commit()
#                 st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                 st.success(get_text("purchased"))
#                 st.rerun()
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 logger.error(f"Error updating inventory from shopping list: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

# def recipe_adjustment_page() -> None:
#     """Adjust recipes based on servings or main ingredient."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     inventory_key = f"inventory_data_{user_id}"
#     try:
#         inventory = DatabaseManager.list_inventory(user_id)
#         st.session_state[inventory_key] = inventory
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading data for adjustment for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     st.header(get_text("adjust_recipe"))
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading recipes for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     if not recipes:
#         st.info(get_text("no_recipes"))
#         return

#     selected_recipe_title = st.selectbox(get_text("select_recipe"), [r.get("title") for r in recipes], key="select_recipe_adjust")
#     if not selected_recipe_title:
#         st.warning(get_text("no_recipe_selected"))
#         return

#     recipe = next(r for r in recipes if r.get("title") == selected_recipe_title)
#     adjustment_type = st.radio(get_text("adjustment_type"), [get_text("by_servings"), get_text("by_main_ingredient")], key="adjustment_type_radio")
#     adjustment_ratio = 1.0

#     try:
#         if adjustment_type == get_text("by_servings"):
#             base_servings = float(recipe.get("servings", 1.0))
#             new_servings = st.number_input(get_text("new_servings"), min_value=0.1, step=0.1, value=base_servings, key="new_servings_input")
#             adjustment_ratio = new_servings / base_servings if base_servings > 0 else 1.0
#         else:
#             main_ingredients = [ing for ing in recipe.get("ingredients", []) if not ing.get("is_spice")]
#             if not main_ingredients:
#                 st.error(get_text("error_ingredients_required"))
#                 return
#             main_ingredient = st.selectbox(get_text("main_ingredient"), [ing.get("name") for ing in main_ingredients], key="main_ingredient_select")
#             selected_ing = next(ing for ing in main_ingredients if ing.get("name") == main_ingredient)
#             base_qty = float(selected_ing.get("quantity", 1.0))
#             new_quantity = st.number_input(get_text("new_quantity"), min_value=0.0, step=0.1, value=base_qty, key="new_quantity_input")
#             adjustment_ratio = new_quantity / base_qty if base_qty > 0 else 1.0
#     except ValueError as e:
#         st.error(get_text("invalid_quantity"))
#         return

#     spice_display_to_key = {
#         get_text("mild"): "mild",
#         get_text("normal"): "normal",
#         get_text("rich"): "rich"
#     }
#     spice_level = st.radio(get_text("spice_level"), [get_text("mild"), get_text("normal"), get_text("rich")], key="spice_level_radio")
#     spice_key = spice_display_to_key.get(spice_level, "normal")
#     spice_factor = {"mild": 0.6, "normal": 0.8, "rich": 1.0}[spice_key]

#     adjusted_recipe = {
#         "id": recipe.get("id"),
#         "title": get_text("adjusted_recipe_title").format(title=recipe.get("title")),
#         "category": recipe.get("category"),
#         "instructions": recipe.get("instructions"),
#         "servings": (recipe.get("servings", 1.0) * adjustment_ratio) if adjustment_type == get_text("by_servings") else recipe.get("servings", 1.0),
#         "ingredients": [],
#         "origin_id": recipe.get("id"),
#         "tag": "adjusted"
#     }

#     for ing in recipe.get("ingredients", []):
#         try:
#             new_qty = max(0.0, float(ing.get("quantity", 0.0)) * adjustment_ratio * (spice_factor if ing.get("is_spice") else 1.0))
#             adjusted_recipe["ingredients"].append({
#                 "name": ing.get("name"),
#                 "quantity": new_qty,
#                 "unit": ing.get("unit"),
#                 "is_spice": ing.get("is_spice", False)
#             })
#         except ValueError:
#             st.error(get_text("invalid_quantity"))
#             return

#     st.session_state["adjusted_recipe"] = adjusted_recipe
#     st.subheader(get_text("adjusted_recipe"))
#     st.write(f"**{get_text('title')}:** {html.escape(adjusted_recipe['title'])}")
#     st.write(f"**{get_text('category')}:** {html.escape(adjusted_recipe.get('category', ''))}")
#     st.write(f"**{get_text('servings')}:** {float(adjusted_recipe.get('servings', 0.0)):.2f}")
#     st.write(f"**{get_text('instructions')}:** {html.escape(adjusted_recipe.get('instructions', ''))}")
#     st.table([
#         {get_text("name"): html.escape(ing["name"]), get_text("quantity"): ing["quantity"],
#          get_text("unit"): ing["unit"], "Spice": "Yes" if ing["is_spice"] else "No"}
#         for ing in adjusted_recipe["ingredients"]
#     ])

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button(get_text("cook_adjusted"), key="cook_adjusted_button"):
#             try:
#                 feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
#                 success, message = consume_ingredients_for_recipe(adjusted_recipe, user_id)
#                 if success:
#                     DatabaseManager.log_cooked_recipe(user_id, adjusted_recipe["origin_id"])
#                     count = DatabaseManager.get_cooked_count(user_id, adjusted_recipe["origin_id"])
#                     stars = calculate_stars(count, recipe.get("is_signature", False))
#                     if stars > calculate_stars(count - 1, recipe.get("is_signature", False)):
#                         st.success(get_text("congrats").format(stars="⭐" * stars, dish=adjusted_recipe["title"]))
#                     st.success(get_text("cook_adjusted_success").format(title=adjusted_recipe["title"]))
#                     st.session_state.pop("adjusted_recipe", None)
#                     st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
#                     st.rerun()
#                 else:
#                     st.error(get_text("cook_adjusted_failed").format(title=adjusted_recipe["title"], error=message.split(": ")[-1]))
#                     if shorts:
#                         st.table([
#                             {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
#                              get_text("have"): f"{s['have_qty']} {s['have_unit']}",
#                              get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
#                             for s in shorts
#                         ])
#             except SQLAlchemyError as e:
#                 logger.error(f"Error cooking adjusted recipe {adjusted_recipe['title']}: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

#     with col2:
#         if st.button(get_text("add_to_shopping_adjusted"), key="add_to_shopping_adjusted_button"):
#             try:
#                 feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
#                 if not feasible:
#                     agg_missing = defaultdict(lambda: {"name": "", "quantity": 0.0, "unit": ""})
#                     for s in shorts:
#                         key = (_norm_name(s["name"]), _norm_unit(s["missing_unit_disp"]))
#                         agg_missing[key]["name"] = s["name"]
#                         agg_missing[key]["quantity"] += s["missing_qty_disp"]
#                         agg_missing[key]["unit"] = s["missing_unit_disp"]
#                     new_shopping_list = list(agg_missing.values())
#                     st.session_state["shopping_list_data"] = new_shopping_list
#                     st.success(get_text("sent_to_shopping"))
#                     st.rerun()
#                 else:
#                     st.info(get_text("all_available"))
#             except SQLAlchemyError as e:
#                 logger.error(f"Error adding adjusted recipe to shopping list: {e}")
#                 st.error(get_text("db_error").format(error=str(e)))

# def food_timeline_page() -> None:
#     """Display cooking history as a timeline."""
#     user_id = current_user_id()
#     if not user_id:
#         st.error(get_text("not_logged_in"))
#         return
#     try:
#         recipes = DatabaseManager.list_recipes(user_id)
#         history = DatabaseManager.list_cooked_history(user_id)
#     except SQLAlchemyError as e:
#         logger.error(f"Error loading data for timeline for user {user_id}: {e}")
#         st.error(get_text("db_error").format(error=str(e)))
#         return

#     st.header(get_text("food_timeline"))
#     if not history:
#         st.info(get_text("no_history"))
#         return

#     recipe_map = {r["id"]: r for r in recipes}
#     search = st.text_input(get_text("search_placeholder"), key="timeline_search", value=st.session_state.get("search_value", ""))
#     st.session_state["search_value"] = search

#     filtered_history = []
#     for entry in history:
#         recipe = recipe_map.get(entry["recipe_id"], {"title": "Unknown", "is_signature": False})
#         count = DatabaseManager.get_cooked_count(user_id, entry["recipe_id"])
#         stars = calculate_stars(count, recipe.get("is_signature", False))
#         entry_data = {
#             "recipe_id": entry["recipe_id"],
#             "title": recipe["title"],
#             "cooked_date": entry["cooked_date"],
#             "stars": stars,
#             "is_signature": recipe.get("is_signature", False)
#         }
#         if not search:
#             filtered_history.append(entry_data)
#         else:
#             search_lower = search.lower()
#             date = datetime.strptime(entry["cooked_date"], "%Y-%m-%d %H:%M:%S")
#             week = date.isocalendar()[1]
#             searches = [s.strip() for s in search_lower.split(",")]
#             match = False
#             for s in searches:
#                 if s.startswith("tag:signature") and entry_data["is_signature"]:
#                     match = True
#                 elif s.startswith("week:") and s[5:].isdigit() and int(s[5:]) == week:
#                     match = True
#                 elif s.startswith("day:") and s[4:] in entry["cooked_date"]:
#                     match = True
#                 elif search_lower in entry_data["title"].lower():
#                     match = True
#             if match:
#                 filtered_history.append(entry_data)

#     if not filtered_history:
#         st.info(get_text("no_entries"))
#         return

#     if st.button(get_text("reset_filter"), key="reset_timeline_filter"):
#         st.session_state["search_value"] = ""
#         st.rerun()

#     dish_counts = Counter(h["title"] for h in filtered_history)
#     if dish_counts:
#         week_start = datetime.now() - timedelta(days=datetime.now().weekday())
#         week_end = week_start + timedelta(days=6)
#         week_history = [
#             h for h in filtered_history
#             if week_start <= datetime.strptime(h["cooked_date"], "%Y-%m-%d %H:%M:%S") <= week_end
#         ]
#         week_counts = Counter(h["title"] for h in week_history)
#         most_common = week_counts.most_common(1)
#         if most_common:
#             st.write(get_text("stats_week").format(
#                 count=len(week_history),
#                 dish=most_common[0][0]
#             ))

#     for entry in sorted(filtered_history, key=lambda x: x["cooked_date"], reverse=True):
#         with st.container():
#             st.markdown('<div class="food-card">', unsafe_allow_html=True)
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.markdown(f'<span class="dish-name">{html.escape(entry["title"])}</span>', unsafe_allow_html=True)
#                 st.write(f"{entry['cooked_date']}")
#             with col2:
#                 st.markdown(f'<span class="stars">{"⭐" * entry["stars"]}</span>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

# def auth_gate_tabs() -> None:
#     """Display authentication tabs for login, register, and reset password."""
#     tabs = st.tabs([get_text("login"), get_text("register"), get_text("reset_password")])
#     with tabs[0]:
#         with st.form(key="login_form"):
#             username = st.text_input(get_text("username"), key="login_username")
#             password = st.text_input(get_text("password"), type="password", key="login_password")
#             if st.form_submit_button(get_text("login_button")):
#                 user_id = DatabaseManager.verify_login(username, password)
#                 if user_id:
#                     st.session_state["user_id"] = user_id
#                     st.session_state["username"] = username
#                     logger.info(f"User {username} logged in successfully")
#                     st.success(f"Welcome, {username}!")
#                     st.rerun()
#                 else:
#                     st.error("Invalid username or password")
#     with tabs[1]:
#         with st.form(key="register_form"):
#             username = st.text_input(get_text("username"), key="register_username")
#             password = st.text_input(get_text("password"), type="password", key="register_password")
#             sec_question = st.text_input(get_text("sec_question"), key="register_sec_question")
#             sec_answer = st.text_input(get_text("sec_answer"), type="password", key="register_sec_answer")
#             if st.form_submit_button(get_text("create_account")):
#                 success, message = DatabaseManager.create_user(username, password, sec_question, sec_answer)
#                 if success:
#                     st.success(message)
#                     user_id = DatabaseManager.verify_login(username, password)
#                     if user_id:
#                         st.session_state["user_id"] = user_id
#                         st.session_state["username"] = username
#                         logger.info(f"User {username} registered and logged in")
#                         st.rerun()
#                 else:
#                     st.error(message)
#     with tabs[2]:
#         with st.form(key="reset_form"):
#             username = st.text_input(get_text("username"), key="reset_username")
#             sec_answer = st.text_input(get_text("sec_answer"), type="password", key="reset_sec_answer")
#             new_password = st.text_input(get_text("new_password"), type="password", key="reset_new_password")
#             if st.form_submit_button(get_text("reset_button")):
#                 if DatabaseManager.reset_password(username, sec_answer, new_password):
#                     st.success("Password reset successfully")
#                     logger.info(f"Password reset for user {username}")
#                 else:
#                     st.error("Invalid username or security answer")

# def main() -> None:
#     """Main application entry point."""
#     st.set_page_config(page_title=APP_TITLE_EN, page_icon="🍽️", layout="wide")
#     inject_css()
#     initialize_session_state()

#     lang = st.session_state.get("language", "English")
#     st.title(get_text("app_title"))

#     if not current_user_id():
#         auth_gate_tabs()
#     else:
#         topbar_account()
#         tabs = st.tabs([
#             get_text("inventory"),
#             get_text("recipes"),
#             get_text("feasibility"),
#             get_text("shopping_list"),
#             get_text("adjust_recipe"),
#             get_text("food_timeline")
#         ])
#         with tabs[0]:
#             inventory_page()
#         with tabs[1]:
#             recipes_page()
#         with tabs[2]:
#             feasibility_page()
#         with tabs[3]:
#             shopping_list_page()
#         with tabs[4]:
#             recipe_adjustment_page()
#         with tabs[5]:
#             food_timeline_page()

# if __name__ == "__main__":
#     main()






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
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables
load_dotenv()

# Thiết lập logging
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

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/recipe_app")
POSTGRES_SUPERUSER = os.getenv("POSTGRES_SUPERUSER", "postgres")
POSTGRES_SUPERUSER_PASSWORD = os.getenv("POSTGRES_SUPERUSER_PASSWORD", "postgres")
ROLE_NAME = "recipe_user"
ROLE_PASSWORD = "secure_password_123"
DB_NAME = "recipe_app"

# Văn bản đa ngôn ngữ
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
        "cook_adjusted_success": "Adjusted recipe '{title}' cooked successfully.",
        "cook_adjusted_failed": "Failed to cook adjusted recipe '{title}': {error}",
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
        "cook_adjusted_success": "Công thức điều chỉnh '{title}' đã nấu thành công.",
        "cook_adjusted_failed": "Không thể nấu công thức điều chỉnh '{title}': {error}",
        "not_logged_in": "Bạn phải đăng nhập để truy cập trang này.",
        "error_title_required": "Tiêu đề công thức là bắt buộc.",
        "error_ingredients_required": "Cần ít nhất một nguyên liệu hợp lệ (với tên và số lượng dương).",
        "duplicate_recipe": "Công thức với tiêu đề này đã tồn tại.",
        "error_invalid_name": "Tên nguyên liệu không hợp lệ: {name}",
        "error_invalid_unit": "Đơn vị không hợp lệ: {unit}",
        "error_negative_qty": "Số lượng phải dương cho nguyên liệu: {name}",
        "save_success": "Công thức '{title}' đã được lưu thành công.",
        "update_success": "Công thức '{title}' đã được cập nhật thành công.",
        "delete_success": "Công thức '{title}' đã được xóa thành công.",
        "save_failed": "Không thể lưu công thức '{title}': {error}",
        "update_failed": "Không thể cập nhật công thức '{title}': {error}",
        "delete_failed": "Không thể xóa công thức '{title}'.",
        "food_timeline": "🍲 Dòng thời gian món ăn",
        "no_history": "Chưa có lịch sử nấu ăn.",
        "no_entries": "Không có mục nào khớp với bộ lọc.",
        "congrats": "Chúc mừng! Bạn đã đạt được {stars} với món {dish} 🎉",
        "signature_dish": "Món tủ",
        "search_placeholder": "Tìm kiếm (ví dụ: tag:signature, week:1, day:2025-09-01)",
        "reset_filter": "🔄 Đặt lại bộ lọc",
        "stats_week": "Tuần này bạn đã nấu {count} món, món thường xuyên nhất: {dish}",
        "db_error": "Lỗi cơ sở dữ liệu: {error}",
        "save_changes": "Save Changes",
        "inventory_updated": "Inventory updated successfully.",
        "db_init_failed": "Failed to initialize database: {error}",
        "invalid_quantity": "Invalid quantity format. Use numbers with optional decimal point or comma."
    }
}

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
    ingredients = relationship("RecipeIngredient", back_populates="recipe")

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

try:
    Base.metadata.create_all(engine)
except Exception as e:
    logger.error(f"Failed to create tables: {e}")
    st.error(get_text("db_error").format(error=str(e)))
    st.stop()

# Danh sách export
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

def get_text(key: str, **kwargs) -> str:
    """Retrieve multilingual text with safe formatting."""
    lang = st.session_state.get("language", "English")
    template = TEXT.get(lang, TEXT["English"]).get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception as e:
            logger.warning(f"i18n fallback for key='{key}': {e}")
            return template
    return template

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

def validate_ingredients(recipe: Dict, inventory_map: Dict[Tuple[str, str], dict]) -> Tuple[bool, Optional[str]]:
    """Validate recipe ingredients and check feasibility against inventory."""
    if not recipe.get("ingredients"):
        return False, get_text("error_ingredients_required")
    
    for ing in recipe.get("ingredients", []):
        name = _norm_name(ing.get("name", ""))
        unit = _norm_unit(ing.get("unit", ""))
        qty = float(ing.get("quantity", 0.0))
        
        if not name or qty <= 0:
            return False, get_text("error_ingredients_required")
        if not DatabaseManager.validate_name(ing.get("name", "")):
            return False, get_text("error_invalid_name").format(name=ing.get("name"))
        if unit not in [_norm_unit(u) for u in VALID_UNITS]:
            return False, get_text("error_invalid_unit").format(unit=ing.get("unit"))
        
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
                
                if not inv_item:
                    raise ValueError(f"Ingredient {ing.get('name')} not found in inventory")
                if inv_item["unit"] != ing.get("unit"):
                    raise ValueError(f"Unit mismatch for {ing.get('name')}")
                if inv_item["quantity"] < qty:
                    raise ValueError(f"Insufficient quantity for {ing.get('name')}")
                
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
        """List user recipes."""
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
        """Create or update a recipe."""
        with Session() as session:
            try:
                if not title.strip():
                    return False, get_text("error_title_required")
                if not any(ing["name"].strip() and ing["quantity"] > 0 for ing in ingredients):
                    return False, get_text("error_ingredients_required")
                
                if session.query(Recipe).filter_by(user_id=user_id, title=title).filter(Recipe.id != recipe_id).first():
                    return False, get_text("duplicate_recipe")
                
                if recipe_id:
                    recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
                    if not recipe:
                        return False, get_text("delete_failed").format(title=title)
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
                
                for ing in ingredients:
                    if not cls.validate_name(ing["name"]):
                        return False, get_text("error_invalid_name").format(name=ing["name"])
                    if _norm_unit(ing["unit"]) not in [_norm_unit(u) for u in VALID_UNITS]:
                        return False, get_text("error_invalid_unit").format(unit=ing["unit"])
                    if ing["quantity"] <= 0:
                        return False, get_text("error_negative_qty").format(name=ing["name"])
                    session.add(RecipeIngredient(
                        recipe_id=recipe.id,
                        name=ing["name"],
                        quantity=ing["quantity"],
                        unit=ing["unit"],
                        is_spice=ing.get("is_spice", False)
                    ))
                
                session.commit()
                logger.info(f"{'Updated' if recipe_id else 'Created'} recipe: {title} for user {user_id}")
                return True, get_text("update_success" if recipe_id else "save_success").format(title=title)
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error saving recipe {title}: {e}")
                return False, get_text("save_failed").format(title=title, error=str(e))

    @classmethod
    def delete_recipe(cls, user_id: int, recipe_id: int) -> bool:
        """Delete a recipe."""
        with Session() as session:
            try:
                recipe = session.query(Recipe).filter_by(id=recipe_id, user_id=user_id).first()
                if recipe:
                    session.delete(recipe)
                    session.commit()
                    logger.info(f"Deleted recipe: id={recipe_id} for user {user_id}")
                    return True
                return False
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error deleting recipe {recipe_id}: {e}")
                return False

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
                ingredient_name = st.text_input(get_text("name"), placeholder=get_text("e.g., chicken"), key="new_ingredient_name")
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
                            if DatabaseManager.delete_recipe(user_id, recipe["id"]):
                                st.success(get_text("delete_success").format(title=recipe["title"]))
                                st.rerun()
                            else:
                                st.error(get_text("delete_failed").format(title=recipe["title"]))
                        except SQLAlchemyError as e:
                            logger.error(f"Error deleting recipe {recipe['title']}: {e}")
                            st.error(get_text("delete_failed").format(title=recipe["title"]))

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
                        if stars > calculate_stars(count - 1, result["recipe"].get("is_signature", False)):
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
    for item in shopping_data:
        name = item.get("name", "").strip()
        quantity = item.get("quantity")
        unit = item.get("unit", "")
        if not name or quantity is None or not unit:
            st.error(get_text("error_ingredients_required"))
            return
        if not DatabaseManager.validate_name(name):
            st.error(get_text("error_invalid_name").format(name=name))
            return
        if _norm_unit(unit) not in [_norm_unit(u) for u in VALID_UNITS]:
            st.error(get_text("error_invalid_unit").format(unit=unit))
            return
        if quantity < 0:
            st.error(get_text("error_negative_qty").format(name=name))
            return
        validated_shopping_data.append({
            "name": name,
            "quantity": float(quantity),
            "unit": unit
        })
    st.session_state["shopping_list_data"] = validated_shopping_data

    purchased_labels = [f"{item['name']} ({item['unit']})" for item in validated_shopping_data if item.get("name") and item.get("unit")]
    purchased_names = st.multiselect(get_text("select_purchased"), options=purchased_labels, key="select_purchased_shopping")

    if st.button(get_text("update_inventory"), key="update_inventory_shopping"):
        with Session() as session:
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
                session.commit()
                st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                st.success(get_text("purchased"))
                st.rerun()
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error updating inventory from shopping list: {e}")
                st.error(get_text("db_error").format(error=str(e)))

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
    adjustment_ratio = 1.0

    try:
        if adjustment_type == get_text("by_servings"):
            base_servings = float(recipe.get("servings", 1.0))
            new_servings = st.number_input(get_text("new_servings"), min_value=0.1, step=0.1, value=base_servings, key="new_servings_input")
            adjustment_ratio = new_servings / base_servings if base_servings > 0 else 1.0
        else:
            main_ingredients = [ing for ing in recipe.get("ingredients", []) if not ing.get("is_spice")]
            if not main_ingredients:
                st.error(get_text("error_ingredients_required"))
                return
            main_ingredient = st.selectbox(get_text("main_ingredient"), [ing.get("name") for ing in main_ingredients], key="main_ingredient_select")
            selected_ing = next(ing for ing in main_ingredients if ing.get("name") == main_ingredient)
            base_qty = float(selected_ing.get("quantity", 1.0))
            new_quantity = st.number_input(get_text("new_quantity"), min_value=0.0, step=0.1, value=base_qty, key="new_quantity_input")
            adjustment_ratio = new_quantity / base_qty if base_qty > 0 else 1.0
    except ValueError as e:
        st.error(get_text("invalid_quantity"))
        return

    spice_display_to_key = {
        get_text("mild"): "mild",
        get_text("normal"): "normal",
        get_text("rich"): "rich"
    }
    spice_level = st.radio(get_text("spice_level"), [get_text("mild"), get_text("normal"), get_text("rich")], key="spice_level_radio")
    spice_key = spice_display_to_key.get(spice_level, "normal")
    spice_factor = {"mild": 0.6, "normal": 0.8, "rich": 1.0}[spice_key]

    adjusted_recipe = {
        "id": recipe.get("id"),
        "title": get_text("adjusted_recipe_title").format(title=recipe.get("title")),
        "category": recipe.get("category"),
        "instructions": recipe.get("instructions"),
        "servings": (recipe.get("servings", 1.0) * adjustment_ratio) if adjustment_type == get_text("by_servings") else recipe.get("servings", 1.0),
        "ingredients": [],
        "origin_id": recipe.get("id"),
        "tag": "adjusted"
    }

    for ing in recipe.get("ingredients", []):
        try:
            new_qty = max(0.0, float(ing.get("quantity", 0.0)) * adjustment_ratio * (spice_factor if ing.get("is_spice") else 1.0))
            adjusted_recipe["ingredients"].append({
                "name": ing.get("name"),
                "quantity": new_qty,
                "unit": ing.get("unit"),
                "is_spice": ing.get("is_spice", False)
            })
        except ValueError:
            st.error(get_text("invalid_quantity"))
            return

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
        if st.button(get_text("cook_adjusted"), key="cook_adjusted_button"):
            try:
                feasible, shorts = recipe_feasibility(adjusted_recipe, user_id)
                success, message = consume_ingredients_for_recipe(adjusted_recipe, user_id)
                if success:
                    DatabaseManager.log_cooked_recipe(user_id, adjusted_recipe["origin_id"])
                    count = DatabaseManager.get_cooked_count(user_id, adjusted_recipe["origin_id"])
                    stars = calculate_stars(count, recipe.get("is_signature", False))
                    if stars > calculate_stars(count - 1, recipe.get("is_signature", False)):
                        st.success(get_text("congrats").format(stars="⭐" * stars, dish=adjusted_recipe["title"]))
                    st.success(get_text("cook_adjusted_success").format(title=adjusted_recipe["title"]))
                    st.session_state.pop("adjusted_recipe", None)
                    st.session_state[inventory_key] = DatabaseManager.list_inventory(user_id)
                    st.rerun()
                else:
                    st.error(get_text("cook_adjusted_failed").format(title=adjusted_recipe["title"], error=message.split(": ")[-1]))
                    if shorts:
                        st.table([
                            {get_text("name"): s["name"], get_text("need"): f"{s['needed_qty']} {s['needed_unit']}",
                             get_text("have"): f"{s['have_qty']} {s['have_unit']}",
                             get_text("missing"): f"{s['missing_qty_disp']} {s['missing_unit_disp']}"}
                            for s in shorts
                        ])
            except SQLAlchemyError as e:
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