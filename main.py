import streamlit as st
from datetime import datetime
from utils import set_background, load_user_data, load_json, save_json, ORDERS_FILE
from landing import landing_page
from signup import signup_page
from login import login_page
from dashboard import welcome_page, rerun

def initialize_session():
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = load_user_data()
    if "is_logged_in" not in st.session_state:
        st.session_state["is_logged_in"] = False
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = ""
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "landing"
    if "cart" not in st.session_state:
        st.session_state["cart"] = []
    if "address" not in st.session_state:
        st.session_state["address"] = ""
    if "cart_quantities" not in st.session_state:
        st.session_state["cart_quantities"] = {}
    if "dashboard_menu_selected" not in st.session_state:
        st.session_state["dashboard_menu_selected"] = 0

def place_order_page(username):
    cart = st.session_state.get("cart", [])
    if not cart:
        st.warning("Your cart is empty. Please add medicines before placing an order.")
        if st.button("Browse Medicines"):
            st.session_state["dashboard_menu_selected"] = 0
            st.session_state["current_page"] = "dashboard"
            st.rerun()
        return

    st.header("Confirm Your Order")
    st.subheader("Order Summary")
    total_amount = 0
    for item in cart:
        st.write(f"- {item['name']} x {item['qty']} = ₹{item['price']*item['qty']}")
        total_amount += item['price'] * item['qty']
    st.write(f"**Total Amount: ₹{total_amount}**")
    st.markdown("---")

    address = st.text_area("Enter Delivery Address", value=st.session_state.get("address", ""), key="order_address_textarea")
    if st.button("Place Order"):
        if not address.strip():
            st.warning("Please enter your delivery address.")
            return
        # Load existing orders
        orders = load_json(ORDERS_FILE)
        # Create new order record
        order = {
            "user": username,
            "items": cart,
            "total": total_amount,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "address": address
        }
        orders.append(order)
        # Save updated orders list
        save_json(ORDERS_FILE, orders)
        # Update session state
        st.session_state["address"] = address
        st.success("Order placed successfully!")
        st.session_state["cart"] = []
        st.session_state["cart_quantities"] = {}
        # Redirect to order history page in dashboard
        st.session_state["dashboard_menu_selected"] = 2  # Order History index
        st.session_state["current_page"] = "dashboard"
        st.rerun()

def main():
    set_background(st)
    initialize_session()
    page = st.session_state.get("current_page", "landing")
    logged_in = st.session_state.get("is_logged_in", False)

    if logged_in:
        if page == "order":
            place_order_page(st.session_state["current_user"])
        else:
            welcome_page()
    else:
        if page == "landing":
            landing_page()
        elif page == "login":
            login_page()
            st.info("Don't have an account? Sign Up below 👇")
            if st.button("Go to Sign Up"):
                st.session_state["current_page"] = "signup"
                rerun(st)
        elif page == "signup":
            signup_page()
            st.info("Already have an account? Login below 🔑")
            if st.button("Go to Login"):
                st.session_state["current_page"] = "login"
                rerun(st)
        else:
            st.session_state["current_page"] = "landing"
            landing_page()

if __name__ == "__main__":
    main()
