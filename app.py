import os
import streamlit as st
from dotenv import load_dotenv

# 1. NEW MODULAR IMPORTS (No 'langchain.chains' needed)
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from sidebar import show_profile, generate_ai_summary

load_dotenv()

st.set_page_config(page_title="Ahan Bose - AI Twin", layout="wide")
st.title("🤖 Ahan Bose: AI Digital Twin ")
# CALL THE SIDEBAR FROM THE OTHER FILE
show_profile()


hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

@st.cache_resource
def setup_vector_db():
    # Load and split docs
    loader = DirectoryLoader('./knowledge_base/', glob="./*.txt", loader_cls=TextLoader)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    
    # Setup Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore.as_retriever()

if not hf_token:
    st.error("Token missing!")
else:
    try:
        retriever = setup_vector_db()

        # 2. SETUP LLM
        llm_endpoint = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task = "conversational",
            huggingfacehub_api_token=hf_token,
            temperature=0.5
        )
        llm = ChatHuggingFace(llm=llm_endpoint)

        # 3. DEFINE THE TEMPLATE
        template = """You are Ahan Bose's AI Twin. Answer based only on the context provided:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        # 4. THE LCEL PIPE CHAIN (The Modern Replacement for RetrievalQA)
        # This builds the chain without needing the 'langchain.chains' module
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # Check if we already have the summary in memory
        if "ai_summary" in st.session_state:
            st.info(st.session_state.ai_summary)
        else:
            # Show a placeholder or instructions
            st.caption("Click below to have AI generate a summary of Ahan's profile.")
            
            # THE TRIGGER BUTTON
            if st.button("✨ Generate AI Summary"):
                with st.spinner("Analyzing profile..."):
                    try:
                        #AI SUMMARY
                        ai_summary = generate_ai_summary(llm)
                        st.write(ai_summary)
       
                        # Store in session state so it stays visible
                        st.session_state.ai_summary = ai_summary
                        st.rerun() # Refresh to show the info box
                    except Exception as e:
                        st.error("Could not reach the brain. Try again later!")
        
        # 5. UI
        query = st.text_input("Ask me something:")
        if st.button("Submit") and query:
            with st.spinner("Processing..."):
                # Simply call invoke on the pipe
                response = rag_chain.invoke(query)
                st.markdown("### Answer:")
                st.write(response)

    except Exception as e:
        st.error(f"Error: {e}")