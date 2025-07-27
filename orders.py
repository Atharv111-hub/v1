import streamlit as st
from datetime import datetime
from utils import load_json, save_json, ORDERS_FILE
from cart import show_cart

def place_order(username):
    # Show cart and ask for address, then place order
    if not show_cart():
        return
    address = st.text_input("Delivery Address", value=st.session_state.get("address", ""), key="order_address")
    if st.button("Place Order", key="place_order_btn"):
        if not address.strip():
            st.warning("Please enter your delivery address.")
            return
        orders = load_json(ORDERS_FILE)
        order = {
            "user": username,
            "items": st.session_state["cart"],
            "total": sum(item["price"] * item["qty"] for item in st.session_state["cart"]),
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "address": address
        }
        orders.append(order)
        save_json(ORDERS_FILE, orders)
        st.session_state["address"] = address
        st.success("Order placed successfully!")
        st.session_state["cart"] = []
        st.session_state["cart_quantities"] = {}
        # Redirect to order history page
        st.session_state["dashboard_menu_selected"] = 2  # Order History index
        st.rerun()

def view_orders(username):
    orders = load_json(ORDERS_FILE)
    user_orders = [o for o in orders if o["user"] == username]
    st.header("Your Orders")
    if not user_orders:
        st.info("No orders yet.")
        return
    for idx, order in enumerate(user_orders, 1):
        st.write(f"Order {idx}:")
        st.write(f"Date: {order.get('datetime', 'N/A')}")
        st.write(f"Address: {order.get('address', 'N/A')}")
        for item in order["items"]:
            st.write(f"- {item['name']} x {item['qty']} = ₹{item['price']*item['qty']}")
        st.write(f"Total: ₹{order['total']}")
        st.markdown("---")

def order_page(username):
    cart = st.session_state.get("cart", [])
    if not cart:
        st.warning("Your cart is empty. Please add items before placing an order.")
        if st.button("Browse Medicines", key="order_browse_meds"):
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
    st.write(f"**Total: ₹{total_amount}**")
    st.markdown("---")

    address = st.text_area("Enter Delivery Address", value=st.session_state.get("address", ""), key="order_address_textarea")
    if st.button("Place Order", key="place_order_btn2", type="primary"):
        if not address.strip():
            st.warning("Please enter your delivery address.")
            return
        orders = load_json(ORDERS_FILE)
        order = {
            "user": username,
            "items": cart,
            "total": total_amount,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "address": address
        }
        orders.append(order)
        save_json(ORDERS_FILE, orders)
        st.session_state["address"] = address
        st.success("Order placed successfully!")
        st.session_state["cart"] = []
        st.session_state["cart_quantities"] = {}
        st.session_state["dashboard_menu_selected"] = 2  # Order History
        st.session_state["current_page"] = "dashboard"
        st.rerun()
