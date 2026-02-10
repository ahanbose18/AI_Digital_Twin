import streamlit as st
import pandas as pd
import os

OFFERS_FILE = "knowledge_base/received_offers.csv"

def show_admin_dashboard():
    st.subheader("🕵️‍♂️ Admin Console")
    
    # 1. Look for password in environment variables (.env locally or Secrets on Cloud)
    # It defaults to "ahan2026" if no variable is found
    correct_password = os.getenv("ADMIN_PASSWORD")
    
    # 2. UI for password entry
    admin_key = st.text_input("Enter Admin Password", type="password")
    
    if admin_key == correct_password:
        st.success("Access Granted")
        
        if os.path.exists(OFFERS_FILE):
            try:
                df = pd.read_csv(OFFERS_FILE)
                
                st.write("### Incoming Offers")
                # Summary Metrics
                c1, c2 = st.columns(2)
                c1.metric("Total Offers", len(df)+1)
                
                # Interactive Table
                st.dataframe(df, use_container_width=True)
                
                # Download Button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Offers CSV",
                    data=csv,
                    file_name="ahan_bose_offers.csv",
                    mime="text/csv"
                )
                
                # Clear Data Button (with double confirmation)
                if st.checkbox("Enable Delete Mode"):
                    if st.button("🗑️ Permanent: Clear All Data"):
                        os.remove(OFFERS_FILE)
                        st.rerun()
            except Exception as e:
                st.error(f"Error reading offers: {e}")
        else:
            st.info("No offers in the database yet.")
            
    elif admin_key:
        st.error("Unauthorized access. Key does not match.")