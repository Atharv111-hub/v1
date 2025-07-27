import json
import os
import base64
from datetime import datetime

USERS_FILE = "users.json"
MEDICINES_FILE = "medicines.json"
ORDERS_FILE = "orders.json"
CONSULTS_FILE = "consultations.json"

def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def load_user_data():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return {}

def save_user_data(user_data):
    with open(USERS_FILE, "w") as file:
        json.dump(user_data, file, indent=2)

def is_valid_email(email):
    if "@" not in email or email.count("@") != 1:
        return False
    local_part, domain_part = email.split("@")
    if not local_part or not domain_part:
        return False
    allowed_local_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-")
    if any(char not in allowed_local_chars for char in local_part):
        return False
    if "." not in domain_part:
        return False
    domain_parts = domain_part.split(".")
    if len(domain_parts) < 2:
        return False
    domain_name = domain_parts[0]
    if not domain_name or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for char in domain_name):
        return False
    for extension in domain_parts[1:]:
        if len(extension) < 2 or not extension.isalpha():
            return False
    return True

def is_valid_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    has_uppercase = False
    has_lowercase = False
    has_digit = False
    has_special = False
    special_characters = "!@#$%^&*()-_+="
    for char in password:
        if char.isupper():
            has_uppercase = True
        elif char.islower():
            has_lowercase = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True
    if not has_uppercase:
        return False, "Password must have at least one uppercase letter."
    if not has_lowercase:
        return False, "Password must have at least one lowercase letter."
    if not has_digit:
        return False, "Password must have at least one digit."
    if not has_special:
        return False, f"Password must have at least one special character: {special_characters}"
    return True, ""

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(st, theme="modern_medical"):
    """
    Set a professional medical-themed background for the medicine delivery app.
    
    Themes available:
    - modern_medical: Modern medical design with animated elements (default)
    - pharmacy_pro: Professional pharmacy theme
    - healthcare_premium: Premium healthcare design
    - medical_clean: Clean medical interface
    - custom_image: Use custom image file
    """
    
    if theme == "modern_medical":
        # Modern medical design with animated elements
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            .stApp {
                background: linear-gradient(135deg, 
                    #f0f8ff 0%, 
                    #e6f3ff 20%, 
                    #ffffff 40%, 
                    #f8fdff 60%, 
                    #eef7ff 80%, 
                    #f5fbff 100%);
                background-attachment: fixed;
                font-family: 'Inter', sans-serif;
            }
            
            /* Animated medical pattern */
            .stApp::before {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: 
                    radial-gradient(circle at 10% 20%, rgba(0, 123, 255, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 80% 80%, rgba(40, 167, 69, 0.06) 0%, transparent 40%),
                    radial-gradient(circle at 40% 40%, rgba(220, 53, 69, 0.04) 0%, transparent 40%);
                animation: pulse 4s ease-in-out infinite;
                pointer-events: none;
                z-index: -2;
            }
            
            /* Floating medical icons */
            .stApp::after {
                content: "💊 🏥 ⚕️ 🚑 💉 🩺";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                font-size: 1.5rem;
                color: rgba(0, 123, 255, 0.1);
                display: flex;
                align-items: center;
                justify-content: space-around;
                flex-wrap: wrap;
                animation: float 6s ease-in-out infinite;
                pointer-events: none;
                z-index: -1;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            
            /* Enhanced component styling */
            .stSelectbox > div > div {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 2px solid rgba(0, 123, 255, 0.1);
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }
            
            .stSelectbox > div > div:hover {
                border-color: rgba(0, 123, 255, 0.3);
                box-shadow: 0 4px 20px rgba(0, 123, 255, 0.1);
            }
            
            .stTextInput > div > div {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 2px solid rgba(0, 123, 255, 0.1);
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }
            
            .stTextInput > div > div:focus-within {
                border-color: rgba(0, 123, 255, 0.5);
                box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
            }
            
            .stButton > button {
                background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 123, 255, 0.2);
            }
            
            .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
                background: linear-gradient(135deg, #0056b3 0%, #004494 100%);
            }
            
            /* Success button variant */
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
            }
            
            .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #20c997 0%, #17a2b8 100%);
                box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
            }
            
            /* Card-like containers */
            .stContainer > div {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 20px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
            }
            
            .stContainer > div:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
            }
            
            /* Header styling */
            h1, h2, h3 {
                color: #2c3e50;
                font-weight: 700;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            /* Custom medical badge */
            .medical-badge {
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                padding: 10px 20px;
                border-radius: 25px;
                font-size: 0.9rem;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
                z-index: 1000;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    
    elif theme == "pharmacy_pro":
        # Professional pharmacy theme with glassmorphism
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, 
                    #667eea 0%, 
                    #764ba2 50%, 
                    #f093fb 100%);
                background-attachment: fixed;
                position: relative;
            }
            
            /* Glassmorphism overlay */
            .stApp::before {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                pointer-events: none;
                z-index: -1;
            }
            
            /* Floating pharmacy elements */
            .stApp::after {
                content: "🏥";
                position: fixed;
                top: 15%;
                right: 15%;
                font-size: 4rem;
                opacity: 0.1;
                animation: rotate 10s linear infinite;
                pointer-events: none;
                z-index: -1;
            }
            
            @keyframes rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            /* Enhanced glassmorphism components */
            .stSelectbox > div > div,
            .stTextInput > div > div {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                backdrop-filter: blur(15px);
                transition: all 0.3s ease;
            }
            
            .stButton > button {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
                backdrop-filter: blur(15px);
                transition: all 0.3s ease;
                font-weight: 600;
            }
            
            .stButton > button:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-3px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    elif theme == "healthcare_premium":
        # Premium healthcare design with medical patterns
        st.markdown(
            """
            <style>
            .stApp {
                background: 
                    linear-gradient(135deg, rgba(16, 71, 156, 0.1) 0%, transparent 50%),
                    linear-gradient(45deg, rgba(25, 135, 84, 0.1) 50%, transparent 100%),
                    linear-gradient(to bottom, #ffffff 0%, #f8f9fa 100%);
                background-attachment: fixed;
            }
            
            /* Medical cross pattern */
            .stApp::before {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: 
                    repeating-linear-gradient(0deg, 
                        rgba(16, 71, 156, 0.02) 0px, 
                        rgba(16, 71, 156, 0.02) 2px, 
                        transparent 2px, 
                        transparent 40px),
                    repeating-linear-gradient(90deg, 
                        rgba(25, 135, 84, 0.02) 0px, 
                        rgba(25, 135, 84, 0.02) 2px, 
                        transparent 2px, 
                        transparent 40px);
                pointer-events: none;
                z-index: -1;
            }
            
            /* Floating medical symbols */
            .stApp::after {
                content: "⚕️";
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 15rem;
                opacity: 0.03;
                pointer-events: none;
                z-index: -1;
            }
            
            /* Premium component styling */
            .stSelectbox > div > div,
            .stTextInput > div > div {
                background: rgba(255, 255, 255, 0.98);
                border-radius: 12px;
                border: 2px solid rgba(16, 71, 156, 0.1);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
            }
            
            .stSelectbox > div > div:hover,
            .stTextInput > div > div:hover {
                border-color: rgba(16, 71, 156, 0.3);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
            }
            
            .stButton > button {
                background: linear-gradient(135deg, #104b9c 0%, #198754 100%);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(16, 71, 156, 0.2);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(16, 71, 156, 0.3);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    elif theme == "medical_clean":
        # Clean medical interface with subtle animations
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(to bottom right, #f8f9fa 0%, #e9ecef 100%);
                background-attachment: fixed;
                position: relative;
            }
            
            /* Subtle medical pattern */
            .stApp::before {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 25% 25%, rgba(0, 123, 255, 0.05) 0%, transparent 25%),
                    radial-gradient(circle at 75% 75%, rgba(40, 167, 69, 0.05) 0%, transparent 25%);
                animation: breathe 4s ease-in-out infinite;
                pointer-events: none;
                z-index: -1;
            }
            
            @keyframes breathe {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            /* Clean component styling */
            .stSelectbox > div > div,
            .stTextInput > div > div {
                background: white;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            
            .stSelectbox > div > div:focus-within,
            .stTextInput > div > div:focus-within {
                border-color: #007bff;
                box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
            }
            
            .stButton > button {
                background: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.75rem 1.5rem;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                background: #0056b3;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
            }
            
            /* Medical info cards */
            .medical-info-card {
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                border-left: 4px solid #007bff;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    elif theme == "custom_image":
        # Option to use custom image (keeping original functionality)
        img_path = "medicine_bg.jpg"  # You can change this filename
        if os.path.exists(img_path):
            img_base64 = get_base64_of_bin_file(img_path)
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpg;base64,{img_base64}");
                    background-attachment: fixed;
                    background-size: cover;
                    background-position: center;
                }}
                
                /* Add overlay for better readability */
                .stApp::before {{
                    content: "";
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(255, 255, 255, 0.8);
                    pointer-events: none;
                    z-index: -1;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning(f"Background image not found at {img_path}. Using default medical gradient theme.")
            set_background(st, "medical_gradient")
    
    else:
        # Default to medical gradient if theme not recognized
        set_background(st, "medical_gradient")

def rerun(st_module):
    """
    Rerun the Streamlit script using the correct function for your Streamlit version.
    """
    try:
        st_module.rerun()
    except AttributeError:
        # For older Streamlit versions
        st_module.experimental_rerun()