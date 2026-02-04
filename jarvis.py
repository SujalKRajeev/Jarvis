import streamlit as st
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --- CONFIGURATION ---
st.set_page_config(page_title="Enterprise Jarvis", page_icon="Tb")
st.title("🤖 Enterprise Jarvis")

# sidebar for keys (Best practice for security)
with st.sidebar:
    st.header("Settings")
    pinecone_api_key = st.text_input("Pinecone API Key", type="password")
    pinecone_index = st.text_input("Pinecone Index Name", value="jarvis")
    # Dropdown to simulate "SaaS" features (Enterprise Context)
    department = st.selectbox("Select Department Context", ["General", "HR Policy", "IT Support"])

if not pinecone_api_key:
    st.warning("Please enter your Pinecone API Key in the sidebar to start.")
    st.stop()

# --- INITIALIZATION ---
# 1. Setup Embeddings (The "Translator" from text to numbers)
# Using a small, fast, local model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Setup Vector Store (The "Brain Storage")
os.environ['PINECONE_API_KEY'] = pinecone_api_key
vectorstore = PineconeVectorStore(index_name=pinecone_index, embedding=embeddings)

# 3. Setup LLM (The "Voice")
# Ensure you have run 'ollama run llama3' in your terminal
llm = ChatOllama(model="llama3", temperature=0)

# --- INGESTION (TEACHING JARVIS) ---
# Simple text area to "teach" Jarvis new things on the fly
with st.expander("📚 Add Knowledge to Jarvis"):
    new_knowledge = st.text_area("Paste company policy or docs here:")
    if st.button("Ingest Data"):
        if new_knowledge:
            with st.spinner("Learning..."):
                # Split text and add to Pinecone
                vectorstore.add_texts([new_knowledge], namespace=department)
                st.success(f"Stored in {department} memory!")

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Ask Jarvis something..."):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate Response
    with st.chat_message("assistant"):
        # Create the RAG Chain
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3, "namespace": department})
        
        prompt_template = ChatPromptTemplate.from_template("""
        Answer the question based strictly on the following context:
        {context}
        
        Question: {input}
        """)
        
        document_chain = create_stuff_documents_chain(llm, prompt_template)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # Run the chain
        response = retrieval_chain.invoke({"input": prompt})
        answer = response["answer"]
        
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})