#  Enterprise Jarvis: Local RAG Assistant

A private, self-hosted AI assistant capable of answering questions based on your custom enterprise data. This project uses **Retrieval-Augmented Generation (RAG)** to combine the reasoning power of **Llama 3** with the long-term memory of **Pinecone**.

##  Features
* **Self-Hosted LLM:** Runs entirely locally using Llama 3 (via Ollama) for privacy.
* **Vector Memory:** Uses Pinecone to store and retrieve knowledge contexts.
* **Interactive UI:** Built with Streamlit for a clean, chat-based experience.
* **RAG Pipeline:** Ingests text, converts it to embeddings, and retrieves relevant answers dynamically.

## Tech Stack
* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **LLM Engine:** Ollama (Llama 3)
* **Orchestration:** LangChain
* **Vector Database:** Pinecone
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)

## Prerequisites
Before running the application, ensure you have the following installed:

1.  **Python 3.10 or higher**
2.  **Ollama** (for running the local LLM)
    * Download from [ollama.com](https://ollama.com)
    * Pull the model: `ollama run llama3`
3.  **Pinecone API Key**
    * Sign up at [pinecone.io](https://pinecone.io) (Free Tier is sufficient).

## Installation

1.  **Clone the repository (or navigate to your project folder):**
    ```bash
    cd path/to/your/project
    ```

2.  **Install the required Python dependencies:**
    ```bash
    pip install streamlit langchain langchain-community langchain-ollama langchain-pinecone sentence-transformers
    ```
    *(Note: If you encounter version conflicts, use the strict installation command found in `requirements.txt` or the project documentation.)*

##  How to Run

1.  **Start the Ollama Server:**
    Ensure Ollama is running in the background. If not, open a terminal and run:
    ```bash
    ollama serve
    ```

2.  **Launch the Application:**
    In a separate terminal window, run the Streamlit app:
    ```bash
    streamlit run jarvis.py
    ```

3.  **Access the UI:**
    The application will open automatically in your browser at `http://localhost:8501`.

## Usage Guide

1.  **Enter Credentials:** Input your Pinecone API Key and Index Name in the sidebar.
2.  **Select Context:** Choose a department (e.g., "HR Policy", "IT Support") to simulate enterprise data segregation.
3.  **Teach Jarvis:** Expand the "Add Knowledge" section, paste text (e.g., a company policy), and click **Ingest Data**.
4.  **Chat:** Type a question related to the ingested text. Jarvis will retrieve the relevant info and answer using Llama 3.

## How It Works (RAG Pipeline)
1.  **Ingestion:** User text is split and converted into vector embeddings using `all-MiniLM-L6-v2`.
2.  **Storage:** Vectors are stored in the Pinecone cloud database.
3.  **Retrieval:** When a user asks a question, the system searches Pinecone for the most similar text chunks.
4.  **Generation:** The retrieved chunks + the user's question are sent to the local Llama 3 model to generate a natural language answer.