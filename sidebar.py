import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def generate_ai_summary(llm):
    """Reads profile.txt and generates a 3-sentence professional summary."""
    try:
        with open("./profile.txt", "r") as f:
            profile_text = f.read()
        
        # Simple Summarization Prompt
        prompt = ChatPromptTemplate.from_template(
            "Summarize the following professional profile into short paragraph not more than 50 words, do not reveal email ID or phone number, and ensure to end"
            "with few sentences highlighting key skills, experience, and projects. "
            "Write in the third person. \n\nProfile: {text}"
        )
        
        # Fast LCEL Chain
        summarizer = prompt | llm | StrOutputParser()
        return summarizer.invoke({"text": profile_text})
    except Exception as e:
        return "AI Summary currently unavailable. Update profile.txt to enable."



def show_profile():
    # --- CUSTOM CSS STYLING ---
    st.markdown("""
        <style>
        /* Target the sidebar container */
        [data-testid="stSidebar"] {
            background-color: #f1f3f5 !important; /* Slightly darker grey for depth */
            border-right: 2px solid #dee2e6;
        }

        /* Force all text in the sidebar to be Dark Grey/Black */
        [data-testid="stSidebar"] .stText, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span {
            color: #212529 !important; /* Professional Dark Grey */
            font-weight: 400;
        }

        /* Style the Subheaders specifically */
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #0d6efd !important; /* Blue for headers */
            font-weight: 700 !important;
        }

        /* Style the Profile Name */
        .profile-name {
            font-size: 26px;
            font-weight: 800;
            color: #1a73e8 !important;
            text-align: center;
            margin-bottom: 10px;
        }

        /* Style the AI Summary Box */
        .stInfo {
            background-color: #ffffff !important;
            color: #212529 !important;
            border: 1px solid #ced4da !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR CONTENT ---
    with st.sidebar:
        # headshot image
        st.image("https://media.licdn.com/dms/image/v2/D5603AQHnuwh4mMnwYg/profile-displayphoto-crop_800_800/B56ZjcS71_HUAI-/0/1756042608528?e=1772064000&v=beta&t=yer-pM8z72mJMF7Yg_nGDSeNCAT3YD2ybpj__AmxKaI", width=150) 
        st.markdown('<p class="profile-name">Ahan Bose</p>', unsafe_allow_html=True)
        
        st.write("📍 **Mumbai, India**")
        st.write("💼 **SPJIMR MBA**")
        
        st.divider()
        
        st.subheader("About Me")
        st.caption("""
            I build intelligent systems using LangChain and Hugging Face. 
            This Digital Twin is powered by a RAG pipeline to answer 
            questions about my career and projects.
        """)
        
        st.divider()
        
        st.subheader("Connect")
        st.markdown('<a href="www.linkedin.com/in/ahan-bose-spjimr" class="social-badge">LinkedIn</a>', unsafe_allow_html=True)
        