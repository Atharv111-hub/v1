import streamlit as st
from datetime import datetime
from utils import load_json, save_json, CONSULTS_FILE

def consult_doctor(username):
    st.header("Consult a Doctor")
    with st.form("consult_form"):
        symptoms = st.text_area("Describe your symptoms")
        preferred_time = st.text_input("Preferred time for consultation (e.g., 5-6pm, Tomorrow morning, etc.)", key="consult_time")
        submit = st.form_submit_button("Request Consultation")
        if submit:
            if not symptoms.strip() or not preferred_time.strip():
                st.warning("Please fill in all fields.")
            else:
                consultations = load_json(CONSULTS_FILE)
                consultation = {
                    "user": username,
                    "symptoms": symptoms,
                    "preferred_time": preferred_time,
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "Requested"
                }
                consultations.append(consultation)
                save_json(CONSULTS_FILE, consultations)
                st.success("Consultation request submitted! A doctor will contact you soon.")

def view_consultations(username):
    consultations = load_json(CONSULTS_FILE)
    user_consults = [c for c in consultations if c["user"] == username]
    st.header("Your Consultation Requests")
    if not user_consults:
        st.info("No consultation requests yet.")
        return
    for idx, c in enumerate(user_consults, 1):
        st.write(f"Request {idx}:")
        st.write(f"Date: {c['datetime']}")
        st.write(f"Symptoms: {c['symptoms']}")
        st.write(f"Preferred Time: {c['preferred_time']}")
        st.write(f"Status: {c.get('status', 'Requested')}")
        st.markdown("---")
