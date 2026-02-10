import streamlit as st
import pandas as pd
import os
from datetime import datetime

OFFERS_FILE = "knowledge_base/received_offers.csv"

def save_offer(data):
    df = pd.DataFrame([data])
    if not os.path.exists(OFFERS_FILE):
        df.to_csv(OFFERS_FILE, index=False)
    else:
        df.to_csv(OFFERS_FILE, mode='a', header=False, index=False)

def show_recruiter_form():
    st.subheader("📩 Job Offer Portal")
    st.caption("Recruiters: Please provide details to initiate a discussion.")
    
    with st.form("job_offer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company Name*")
            position = st.text_input("Position*")
        with col2:
            ctc = st.text_input("Offered CTC")
            joining = st.date_input("Target Joining Date")
        
        jd_link = st.text_input("Link to JD (LinkedIn/Google Drive)")
        notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("Submit Offer to Ahan")
        
        if submitted:
            if company and position:
                offer_data = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Company": company,
                    "Position": position,
                    "CTC": ctc,
                    "Joining": joining,
                    "JD_Link": jd_link,
                    "Notes": notes,
                    "Status": "Pending"
                }
                save_offer(offer_data)
                st.success("🎉 Offer recorded! Ahan will be notified.")
            else:
                st.error("Please fill in the required fields (*)")