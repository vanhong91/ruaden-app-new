# main.py
import streamlit as st
import sqlite3
from database import DatabaseManager
from ui import (
    inject_css,
    auth_gate_tabs,
    topbar_account,
    inventory_page,
    recipes_page,
    feasibility_page,
    shopping_list_page,
    recipe_adjustment_page,
    food_timeline_page,
    get_text,
)

# Set page configuration
st.set_page_config(page_title=get_text("app_title"), page_icon="🍳", layout="wide")

def ensure_auth_state():
    """Initialize session state variables if not present."""
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
            "ingredients": [{"name": "", "quantity": 0.0, "unit": "piece", "is_spice": False}],
        },
        "shopping_list_data": [],
        "adjusted_recipe": None,
        "inventory_key": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    try:
        DatabaseManager.init_db()
    except sqlite3.Error as e:
        st.error(get_text("db_error").format(error=e))
        st.stop()

    inject_css()
    ensure_auth_state()

    if st.session_state.user_id:
        st.session_state.inventory_key = f"inventory_data_{st.session_state.user_id}"

    try:
        with DatabaseManager.get_db_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1;")
    except sqlite3.Error as e:
        st.error(get_text("db_error").format(error=e))
        st.stop()

    if not st.session_state.user_id or not DatabaseManager.validate_user_id(st.session_state.user_id):
        auth_gate_tabs()
        return

    topbar_account()
    tab_titles = [
        get_text("inventory"),
        get_text("recipes"),
        get_text("feasibility"),
        get_text("shopping_list"),
        get_text("adjust_recipe"),
        get_text("food_timeline"),
    ]
    tabs = st.tabs(tab_titles)
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