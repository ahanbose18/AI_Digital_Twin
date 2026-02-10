import streamlit as st
import os
from dotenv import load_dotenv
from sidebar import generate_ai_summary,show_profile
from brain import setup_vector_db, get_llm, get_rag_chain
from recruiter_view import show_recruiter_form
from admin_view import show_admin_dashboard
#from admin_view import show_admin_dashboard

# Load Env & Config
load_dotenv()
st.set_page_config(page_title="Ahan Bose - AI Twin", layout="wide")
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize Backend
if not hf_token:
    st.error("Hugging Face Token missing! Check your .env or Streamlit Secrets.")
    st.stop()

# Build the brain
retriever = setup_vector_db()
llm = get_llm(hf_token)
rag_chain = get_rag_chain(retriever, llm)

# 1. Sidebar
#generate_ai_summary(llm)
show_profile()
# 2. Main UI Navigation
st.title("🤖 Ahan Bose: AI Digital Twin")

tabs = st.tabs(["💬 Chat with Me", "💼 Recruiter Portal", "🔐 Admin"])

with tabs[0]:
    # Chat Logic
    # 1. Sidebar
    st.subheader("🤖 AI Summary")
        
    # Check if summary already exists in memory
    if "ai_summary" in st.session_state:
        st.info(st.session_state.ai_summary)
        if st.button("🔄 Regenerate"):
            del st.session_state.ai_summary
            st.rerun()
    else:
        st.caption("Click to generate a summary of Ahan's profile using AI.")
        if st.button("✨ Generate Summary"):
            with st.spinner("Analyzing profile..."):
                try:
                    summary = generate_ai_summary(llm)
                    st.session_state.ai_summary = summary
                    st.success("Summary generated! Scroll up to view.")
                except Exception as e:
                    st.error(f"Error generating summary: {e}")
      
    query = st.text_input("Ask me about my experience, skills, or projects:")
    if st.button("Submit") and query:
        with st.spinner("Thinking..."):
            response = rag_chain.invoke(query)
            st.markdown("### Answer:")
            st.write(response)

with tabs[1]:
    show_recruiter_form()

with tabs[2]:
    show_admin_dashboard()