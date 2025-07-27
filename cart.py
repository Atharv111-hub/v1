import streamlit as st
import datetime

def top_bar():
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
        <h3 style="color: #1f77b4; margin: 0;">🏥 MediCare Delivery System</h3>
    </div>
    """, unsafe_allow_html=True)

def show_cart():
    top_bar()
    st.title("🛒 Your Cart")
    cart = st.session_state.get("cart", [])
    if not cart:
        st.info("🛍️ Your cart is empty. Start shopping to add medicines!")
        if st.button("Browse Medicines", key="browse_meds", type="primary", use_container_width=True):
            st.session_state["dashboard_menu_selected"] = 0  # Navigate to medicines page
            st.rerun()
        return False

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Items in Cart", len(cart))
    with col2:
        total_qty = sum(item['qty'] for item in cart)
        st.metric("Total Quantity", total_qty)
    with col3:
        total_amount = sum(item['price'] * item['qty'] for item in cart)
        st.metric("Total Amount", f"₹{total_amount}")

    st.divider()
    for i, item in enumerate(cart):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{item['name']}**")
                st.write(f"Price: ₹{item['price']} per unit")
                expiry_date = item.get('expiry_date', 'Not specified')
                st.write(f"Expiry: {expiry_date}")
            with col2:
                new_qty = st.number_input(
                    "Qty",
                    min_value=1,
                    max_value=99,
                    value=item['qty'],
                    key=f"qty_{i}"
                )
                if new_qty != item['qty']:
                    cart[i]['qty'] = new_qty
                    st.session_state["cart"] = cart
                    st.rerun()
            with col3:
                subtotal = item['price'] * item['qty']
                st.write(f"**₹{subtotal}**")
            with col4:
                if st.button("Remove", key=f"remove_{i}", type="secondary"):
                    cart.pop(i)
                    st.session_state["cart"] = cart
                    st.rerun()
        st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Continue Shopping", key="continue_shopping", use_container_width=True):
            st.session_state["dashboard_menu_selected"] = 0
            st.rerun()
    with col2:
        if st.button("Clear Cart", use_container_width=True, type="secondary"):
            st.session_state["cart"] = []
            st.session_state["cart_quantities"] = {}
            st.rerun()
    with col3:
        if st.button("Order Now", key="order_now", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "order"
            st.rerun()

    st.success(f"**Total Amount: ₹{total_amount}**")
    return True

def get_expiry_status(expiry_date_str):
    try:
        expiry_parts = expiry_date_str.split('-')
        if len(expiry_parts) == 3:
            expiry_year = int(expiry_parts[0])
            expiry_month = int(expiry_parts[1])
            expiry_day = int(expiry_parts[2])
            today = datetime.datetime.now()
            expiry_date = datetime.datetime(expiry_year, expiry_month, expiry_day)
            days_until_expiry = (expiry_date - today).days
            if days_until_expiry < 0:
                return "⚠️ EXPIRED"
            elif days_until_expiry <= 30:
                return f"⏰ Expires in {days_until_expiry} days"
            else:
                return "✅ Fresh"
    except Exception:
        return "📅 Date format invalid"
    return "📅 Unknown"
