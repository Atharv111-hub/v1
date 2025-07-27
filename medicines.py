import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json
from dataclasses import dataclass
from utils import load_json, MEDICINES_FILE

ITEMS_PER_PAGE = 20
CACHE_DURATION = 300  # 5 minutes

@dataclass
class Medicine:
    id: str
    name: str
    description: str
    category: str
    price: float
    stock: int
    expiry_date: Optional[str] = str
    manufacturer: Optional[str] = None
    requires_prescription: bool = False

class MedicineManager:
    def __init__(self):
        self._cache = {}
        self._cache_time = {}

    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_time:
            return False
        return (datetime.now() - self._cache_time[key]).seconds < CACHE_DURATION

    def get_medicines(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        cache_key = "medicines"
        if not force_refresh and self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        try:
            medicines = load_json(MEDICINES_FILE)
            if not medicines:
                return []
            valid_medicines = []
            for med in medicines:
                if self._validate_medicine(med):
                    valid_medicines.append(med)
            self._cache[cache_key] = valid_medicines
            self._cache_time[cache_key] = datetime.now()
            return valid_medicines
        except Exception as e:
            st.error(f"Error loading medicines: {str(e)}")
            return []

    def _validate_medicine(self, medicine: Dict[str, Any]) -> bool:
        required_fields = ['name', 'price', 'stock','expiry_date']
        return all(field in medicine for field in required_fields)

    def filter_medicines(self, medicines: List[Dict[str, Any]],
                        search_term: str = "",
                        category: str = "All",
                        in_stock_only: bool = True) -> List[Dict[str, Any]]:
        filtered = []
        for med in medicines:
            # Search filter
            if search_term and not self._matches_search(med, search_term):
                continue
            # Category filter
            if category != "All" and med.get("category", "Other") != category:
                continue
            # Stock filter
            if in_stock_only and med.get("stock", 0) <= 0:
                continue
            filtered.append(med)
        return filtered

    def is_expired(self, medicine: Dict[str, Any], today: Optional[datetime.date] = None) -> bool:
        try:
            if "expiry_date" not in medicine:
                return False
            if not today:
                today = datetime.today().date()
            expiry_date = datetime.strptime(medicine["expiry_date"], "%Y-%m-%d").date()
            return expiry_date < today
        except (ValueError, TypeError):
            return False

    def _matches_search(self, medicine: Dict[str, Any], search_term: str) -> bool:
        search_lower = search_term.lower()
        searchable_fields = [
            medicine.get("name", ""),
            medicine.get("description", ""),
            medicine.get("manufacturer", ""),
            medicine.get("category", "")
        ]
        return any(search_lower in field.lower() for field in searchable_fields)

def create_medicine_css():
    st.markdown("""
        <style>
        .med-card {
            padding: 20px;
            margin: 15px 0;
            border-radius: 15px;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .med-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }
        .med-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .med-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #2d3748;
            margin: 0;
        }
        .med-category {
            background: #4299e1;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }
        .med-expired {
            background: #e53e3e;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
            margin-left: 8px;
        }
        .med-description {
            color: #4a5568;
            font-size: 0.95em;
            margin-bottom: 12px;
            line-height: 1.5;
        }
        .med-details {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .price-tag {
            font-size: 1.1em;
            font-weight: 600;
            color: #38a169;
        }
        .stock-info {
            font-size: 0.9em;
            color: #718096;
        }
        .stock-low {
            color: #e53e3e;
            font-weight: 500;
        }
        .stock-out {
            color: #e53e3e;
            font-weight: 600;
        }
        .search-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .filter-row {
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        .cart-summary {
            background: #e6fffa;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #38b2ac;
            margin: 10px 0;
        }
        .prescription-warning {
            background: #fef5e7;
            color: #744210;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9em;
            margin-top: 8px;
        }
        .expiry-warning {
            background: #fed7d7;
            color: #742a2a;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9em;
            margin-top: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

def display_medicine_card(medicine: Dict[str, Any], expired: bool = False, show_expiry: bool = False):
    key = f"qty_{medicine.get('id', medicine.get('name', 'unknown'))}"
    default_qty = st.session_state.get("cart_quantities", {}).get(key, 0)

    st.markdown('<div class="med-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="med-header">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="med-title">{medicine.get("name", "Unknown")}</h3>', unsafe_allow_html=True)
        st.markdown(f'<span class="med-category">{medicine.get("category", "Other")}</span>', unsafe_allow_html=True)
        if expired:
            st.markdown(f'<span class="med-expired">not available</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    description = medicine.get("description", "No description available.")
    st.markdown(f'<div class="med-description">{description}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        price = medicine.get("price", 0)
        st.markdown(f'<div class="price-tag">₹{price:.2f} per unit</div>', unsafe_allow_html=True)
    with col2:
        stock = medicine.get("stock", 0)
        if stock == 0:
            stock_class = "stock-out"
            stock_text = "Out of Stock"
        elif stock <= 5:
            stock_class = "stock-low"
            stock_text = f"Low Stock: {stock}"
        else:
            stock_class = "stock-info"
            stock_text = f"In Stock: {stock}"
        st.markdown(f'<div class="{stock_class}">{stock_text}</div>', unsafe_allow_html=True)
    with col3:
        if expired:
            st.markdown('<div style="color: #e53e3e; font-weight: 600;">not available</div>', unsafe_allow_html=True)
        elif stock > 0:
            qty = st.number_input(
                "Quantity",
                min_value=0,
                max_value=stock,
                value=default_qty,
                key=key,
                help=f"Maximum available: {stock}"
            )
            if "cart_quantities" not in st.session_state:
                st.session_state["cart_quantities"] = {}
            st.session_state["cart_quantities"][key] = qty
        else:
            st.markdown('<div style="color: #e53e3e; font-weight: 600;">Unavailable</div>', unsafe_allow_html=True)

    if medicine.get("manufacturer"):
        st.caption(f"🏭 Manufacturer: {medicine.get('manufacturer')}")
    if medicine.get("requires_prescription"):
        st.markdown(
            '<div class="prescription-warning">⚠️ Prescription required for this medicine</div>',
            unsafe_allow_html=True
        )

    # Expiry date info (always show if requested, else show warnings for expired/expiring)
    if medicine.get("expiry_date"):
        try:
            expiry_date = datetime.strptime(medicine["expiry_date"], "%Y-%m-%d").date()
            days_to_expiry = (expiry_date - datetime.today().date()).days
            if show_expiry or expired or days_to_expiry <= 30:
                if expired:
                    st.markdown(
                        f'<div class="not avalable-warning">❌ medicine is not avalable </div>',
                        unsafe_allow_html=True
                    )
                elif days_to_expiry <= 30:
                    st.markdown(
                        f'<div class="not avalable">⚠️ Expires in {days_to_expiry} days ({expiry_date})</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div style="color:#555;font-size:0.95em;margin-top:8px;">Expiry Date: {expiry_date}</div>',
                        unsafe_allow_html=True
                    )
        except Exception:
            st.markdown(
                f'<div style="color:#555;font-size:0.95em;margin-top:8px;">Expiry Date: {medicine.get("expiry_date")}</div>',
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

def add_selected_to_cart(medicines: List[Dict[str, Any]], medicine_manager: MedicineManager):
    cart_items = []
    today = datetime.today().date()
    for med in medicines:
        key = f"qty_{med.get('id', med.get('name', 'unknown'))}"
        qty = st.session_state.get("cart_quantities", {}).get(key, 0)
        expired = medicine_manager.is_expired(med, today)
        if expired:
            continue
        if qty > 0:
            existing_item = next((item for item in st.session_state["cart"]
                                if item.get("id") == med.get("id")), None)
            if existing_item:
                existing_item["qty"] += qty
            else:
                cart_items.append({
                    "id": med.get("id", ""),
                    "name": med.get("name", ""),
                    "price": med.get("price", 0),
                    "qty": qty,
                    "category": med.get("category", "Other"),
                    "expiry_date": med.get("expiry_date", None)  # ensure expiry is in cart entry
                })
    if cart_items:
        st.session_state["cart"].extend(cart_items)
        st.success(f"🛒 Added {len(cart_items)} item(s) to cart!")
        total_items = sum(item.get("qty", 0) for item in st.session_state["cart"])
        total_price = sum(item.get("price", 0) * item.get("qty", 0) for item in st.session_state["cart"])
        st.markdown(f"""
            <div class="cart-summary">
                <strong>🛒 Cart Summary:</strong><br>
                Items: {total_items}<br>
                Total: ₹{total_price:.2f}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please select at least one non-expired medicine with quantity greater than zero.")

def show_medicines(show_expiry=False):
    create_medicine_css()
    medicine_manager = MedicineManager()
    medicines = medicine_manager.get_medicines()
    if not medicines:
        st.warning("⚠️ No medicines found. Please ensure 'medicines.json' exists and has valid data.")
        return
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input(
            "🔍 Search medicines",
            placeholder="Search by name, description, or manufacturer...",
            key="enhanced_search",
            help="Search across medicine name, description, manufacturer, and category"
        )
    with col2:
        if st.button("🔄 Refresh Data", help="Refresh medicine data"):
            medicine_manager.get_medicines(force_refresh=True)
            st.experimental_rerun()
    categories = ["All"] + sorted(set(med.get("category", "Other") for med in medicines))
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        category_filter = st.selectbox("📂 Category", categories, key="enhanced_category")
    with col2:
        in_stock_only = st.checkbox("📦 In Stock Only", value=True, key="enhanced_stock")
    with col3:
        sort_by = st.selectbox("🔄 Sort By", ["Name", "Price", "Stock"], key="sort_by")
    st.markdown('</div>', unsafe_allow_html=True)
    filtered_medicines = medicine_manager.filter_medicines(
        medicines, search_term, category_filter, in_stock_only
    )
    if sort_by == "Price":
        filtered_medicines.sort(key=lambda x: x.get("price", 0))
    elif sort_by == "Stock":
        filtered_medicines.sort(key=lambda x: x.get("stock", 0), reverse=True)
    else:  # Name
        filtered_medicines.sort(key=lambda x: x.get("name", ""))
    st.markdown(f"**Found {len(filtered_medicines)} medicine(s)**")
    if not filtered_medicines:
        st.info("🔍 No medicines match your search criteria. Try adjusting your filters.")
        return
    total_pages = max(1, (len(filtered_medicines) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    if total_pages > 1:
        page = st.selectbox(f"📄 Page (1 of {total_pages})", range(1, total_pages + 1), key="page_select") - 1
        start_idx = page * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_medicines = filtered_medicines[start_idx:end_idx]
        st.info(f"Showing {start_idx + 1}-{min(end_idx, len(filtered_medicines))} of {len(filtered_medicines)} medicines")
    else:
        page_medicines = filtered_medicines
    today = datetime.today().date()
    for med in page_medicines:
        expired = medicine_manager.is_expired(med, today)
        display_medicine_card(med, expired=expired, show_expiry=show_expiry)
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🛒 Add Selected to Cart", type="primary", key="add_to_cart_btn"):
            add_selected_to_cart(page_medicines, medicine_manager)
    with col2:
        if st.button("🗑️ Clear Selections", help="Clear all quantity selections"):
            for med in page_medicines:
                key = f"qty_{med.get('id', med.get('name', 'unknown'))}"
                st.session_state["cart_quantities"][key] = 0
            st.experimental_rerun()

def show_enhanced_medicines():
    return show_medicines(show_expiry=True)
