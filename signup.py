import streamlit as st
from utils import is_valid_email, is_valid_password, save_user_data, rerun


def signup_page():
    st.header("📝 Create an Account")
    st.markdown(
        """
        <style>
        .form-container {
        max-width: 450px;
        margin: auto;
        }
        .password-strength {
        font-size: 0.9rem;
        margin-top: -10px;
        margin-bottom: 10px;
        }
        .error-msg {
        color: #e53e3e;
        font-weight: 600;
        margin-bottom: 10px;
        }
        .success-msg {
        color: #38a169;
        font-weight: 600;
        margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    with st.container():
        with st.form("signup_form", clear_on_submit=False):
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            username = st.text_input("Username", max_chars=20, help="Choose a unique username")
            email = st.text_input("Email", help="Enter a valid email address")
            password = st.text_input("Password", type="password", help="At least 6 chars, uppercase, digit & special char")

            error_msgs = []
            if username and username in st.session_state.get("user_data", {}):
                error_msgs.append("⚠️ Username already exists.")
            if email and not is_valid_email(email):
                error_msgs.append("❌ Invalid email format.")
            if password:
                valid_pwd, pwd_msg = is_valid_password(password)
                if not valid_pwd:
                    error_msgs.append(f"❌ {pwd_msg}")

            if password:
                strength_color = "#38a169" if valid_pwd else "#e53e3e"
                st.markdown(f'<div class="password-strength" style="color:{strength_color}">Password check: {"Strong" if valid_pwd else "Weak"}</div>', unsafe_allow_html=True)

            if error_msgs:
                for msg in error_msgs:
                    st.markdown(f'<div class="error-msg">{msg}</div>', unsafe_allow_html=True)

            signup_button = st.form_submit_button("Sign Up")
            st.markdown('</div>', unsafe_allow_html=True)

            if signup_button:
                if not username or not email or not password:
                    st.warning("⚠️ Please fill in all fields.")
                elif error_msgs:
                    st.warning("⚠️ Please fix the errors above before submitting.")
                else:
                    if "user_data" not in st.session_state:
                        st.session_state["user_data"] = {}
                    st.session_state["user_data"][username] = {
                        "email": email,
                        "password": password,
                        "role": "user"  # Assign user role on signup
                    }
                    save_user_data(st.session_state["user_data"])
                    st.success("🎉 Signup successful! Please login.")
                    st.session_state["current_page"] = "login"
                    rerun(st)
