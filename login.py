import streamlit as st
from utils import rerun, load_user_data

def login_page():
    
    st.header("🔐 Login to Your Account")
    # ... styling ...
    with st.form("login_form"):
        username = st.text_input("Username", max_chars=20)
        password = st.text_input("Password", type="password", key="login_password")
        login_button = st.form_submit_button("Login")
        # Always reload user data from file
        st.session_state["user_data"] = load_user_data()
        if login_button:
            if not username or not password:
                st.warning("⚠️ Please fill in all fields.")
            elif username not in st.session_state["user_data"]:
                st.error("❌ User not found.")
            elif st.session_state["user_data"][username]["password"] != password:
                st.error("❌ Incorrect password.")
            else:
                user_info = st.session_state["user_data"][username]
                st.success(f"✅ Welcome back, **{username}**!")
                st.session_state["is_logged_in"] = True
                st.session_state["current_user"] = username
                st.session_state["current_role"] = user_info.get("role", "user")
                st.session_state["current_page"] = "dashboard"
                rerun(st)
