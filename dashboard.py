import streamlit as st
import logging
from utils import rerun
from medicines import show_medicines
from orders import place_order, view_orders
from consult import consult_doctor, view_consultations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Session Management Functions
def initialize_session():
    """Initialize session state with default values"""
    defaults = {
        "is_logged_in": False,
        "current_user": "",
        "cart": [],
        "cart_quantities": {},
        "current_page": "landing",
        "user_preferences": {},
        "last_activity": None,
        "dashboard_menu_selected": 0
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def clear_session():
    """Clear session state data"""
    keys_to_clear = [
        "is_logged_in", "current_user", "cart",
        "cart_quantities", "user_preferences", "dashboard_menu_selected"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            if key in ["cart", "cart_quantities", "user_preferences"]:
                st.session_state[key] = {} if key != "cart" else []
            elif key == "dashboard_menu_selected":
                st.session_state[key] = 0
            else:
                st.session_state[key] = "" if key == "current_user" else False
    st.session_state["current_page"] = "landing"

# UI Styling Functions
def apply_background_theme():
    """Apply a professional medical background theme with clear visibility"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main background styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Add subtle medical pattern overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 2px, transparent 2px),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 2px, transparent 2px),
            radial-gradient(circle at 40% 40%, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 50px 50px, 60px 60px, 30px 30px;
        background-position: 0 0, 30px 30px, 15px 15px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* Main content container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ffffff, #f0f8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        opacity: 0.95;
        font-weight: 400;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(240,248,255,0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Content area styling */
    .block-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.3);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .stWarning {
        background: rgba(255, 152, 0, 0.1);
        border: 1px solid rgba(255, 152, 0, 0.3);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    /* Spinner styling */
    .stSpinner {
        color: #667eea;
    }
    
    /* Sidebar menu styling */
    .sidebar-menu {
        padding: 1rem 0;
    }
    
    .menu-section {
        margin-bottom: 1.5rem;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .menu-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #4a5568;
        margin-bottom: 0.5rem;
    }
    
    /* User welcome styling */
    .user-welcome {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Cart indicator */
    .cart-indicator {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }
    
    /* Medical icons enhancement */
    .medical-icon {
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .header-subtitle {
            font-size: 1rem;
        }
        .main-header {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Create the main header with medical theme"""
    apply_background_theme()
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.write("")  # Empty space instead of image
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1 class="header-title">🏥 MediCare Plus</h1>
            <p class="header-subtitle">Your trusted medicine delivery service</p>
            <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                💊 Fast Delivery • 👨‍⚕️ Expert Consultation
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        username = st.session_state.get("current_user", "")
        if username:
            st.markdown(f"""
            <div class="user-welcome">
                <div style="font-size: 1.5rem;">👋</div>
                <div style="font-weight: 500; margin-top: 0.5rem;">Welcome</div>
                <div style="font-weight: 600; color: #f0f8ff;">{username}</div>
            </div>
            """, unsafe_allow_html=True)

def create_sidebar_menu():
    """Create the sidebar navigation menu"""
    st.sidebar.markdown("""
    <style>
    .sidebar-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div class="sidebar-title">
        🏥 MediCare Navigation
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-menu">', unsafe_allow_html=True)
    
    username = st.session_state.get("current_user", "Guest")
    cart_count = len(st.session_state.get("cart", []))
    
    # User info section
    st.sidebar.markdown(f"""
    <div class="menu-section">
        <div style="text-align: center; font-weight: 600; color: #667eea;">
            👤 {username}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cart indicator
    if cart_count > 0:
        st.sidebar.markdown(f"""
        <div class="cart-indicator">
            🛒 Cart: {cart_count} items
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Navigation menu
    menu_options = [
        ("🏪 Browse Medicines", "Show Medicines"),
        ("🛒 Cart & Order", "Cart & Place Order"),
        ("📦 Order History", "Order History"),
        ("👨‍⚕️ Consult Doctor", "Consult a Doctor"),
        ("📋 Consultations", "Consultation History")
    ]
    
    menu_labels = [option[0] for option in menu_options]
    menu_values = [option[1] for option in menu_options]
    
    selected_index = st.sidebar.radio(
        "**📋 Menu Options**",
        range(len(menu_options)),
        format_func=lambda x: menu_labels[x],
        index=st.session_state.get("dashboard_menu_selected", 0),
        key="dashboard_menu_radio"
    )
    
    st.session_state["dashboard_menu_selected"] = selected_index
    
    st.sidebar.markdown("---")
    
    # Logout section
    st.sidebar.markdown("""
    <div class="menu-section">
        <div style="text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 1rem;">
            Session Management
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout", help="Logout from your account", type="secondary"):
        st.sidebar.warning("Are you sure you want to logout?")
        if st.sidebar.button("✅ Yes, Logout", type="primary"):
            clear_session()
            st.success("Logged out successfully!")
            rerun(st)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    return menu_values[selected_index]

# Page Configuration Function
def setup_page_config():
    """Setup streamlit page configuration"""
    try:
        st.set_page_config(
            page_title="MediCare Plus - Medicine Delivery",
            page_icon="🏥",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except Exception as e:
        logger.warning(f"Page config already set: {e}")

# Menu Handling Functions
def handle_menu_selection(menu, username):
    """Handle different menu selections"""
    # Add a container for better content organization
    with st.container():
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        try:
            if menu == "Show Medicines":
                with st.spinner("🔍 Loading medicines..."):
                    show_medicines(show_expiry=True)
            elif menu == "Cart & Place Order":
                with st.spinner("🛒 Loading cart..."):
                    from cart import show_cart
                    show_cart()
            elif menu == "Order History":
                with st.spinner("📦 Loading order history..."):
                    view_orders(username)
            elif menu == "Consult a Doctor":
                with st.spinner("👨‍⚕️ Loading consultation page..."):
                    consult_doctor(username)
            elif menu == "Consultation History":
                with st.spinner("📋 Loading consultation history..."):
                    view_consultations(username)
            else:
                st.error("❌ Invalid menu selection")
                logger.error(f"Invalid menu selection: {menu}")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            logger.error(f"Error in menu selection {menu}: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def run_dashboard():
    """Main dashboard function"""
    if not st.session_state.get("is_logged_in", False):
        st.error("🔐 Please login to access the dashboard")
        return
    
    create_header()
    
    username = st.session_state.get("current_user", "unknown")
    if username == "unknown":
        st.error("⚠️ User session invalid. Please login again.")
        return
    
    menu = create_sidebar_menu()
    handle_menu_selection(menu, username)

# Deprecated function wrappers for backward compatibility
def top_bar():
    """Deprecated function - use create_header() instead"""
    logger.warning("top_bar() is deprecated. Use create_header()")
    create_header()

def sidebar_menu():
    """Deprecated function - use create_sidebar_menu() instead"""
    logger.warning("sidebar_menu() is deprecated. Use create_sidebar_menu()")
    return create_sidebar_menu()

def welcome_page():
    """Main welcome page function"""
    initialize_session()
    setup_page_config()
    run_dashboard()

# Main execution
if __name__ == "__main__":
    welcome_page()