VisAgent

VisAgent is a multi-modal AI agent that integrates text, PDF, and image ingestion with retrieval-augmented generation (RAG) and vision-based reasoning, powered by GroqLLM. It provides an end-to-end framework for querying documents, analyzing images, and generating intelligent responses.

Features:

* Text and PDF ingestion into a vector store (Chroma DB) for fast retrieval.
* Vision processing for image understanding and captioning.
* Retrieval-Augmented Generation (RAG) for context-aware answers.
* LLM integration with GroqLLM for reasoning and response generation.
* Async API using FastAPI for ingestion and querying.

Project Structure:

* main.py                 # FastAPI server entrypoint
* requirements.txt        # Python dependencies
* .gitignore
* README.md
* src/

  * nodes/               # RAG, Vision, and Response nodes
  * rag\_node.py
  * vision\_node.py
  * response\_node.py
  * llms/                # LLM wrappers (GroqLLM)
  * utils/               # File loaders, logging, helpers
  * graphs/              # GraphBuilder for AI workflow
* models/                 # Pretrained models
* data/                   # Optional: local storage for uploads

Installation:

1. Clone the repository
   git clone [https://github.com/YourUsername/VisAgent.git](https://github.com/YourUsername/VisAgent.git)
   cd VisAgent

2. Create a virtual environment and activate
   python -m venv .venv

   # Windows

   .venv\Scripts\activate

   # Linux/Mac

   source .venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Download or place pretrained models in 'models/' (e.g., 'all-MiniLM-L6-v2').

Running the Server:

* Start the FastAPI server:
  uvicorn main\:app --reload --port 8000

Endpoints:

* POST /ingest — Upload a PDF, TXT, or image for ingestion.
* POST /ask — Query the AI agent with text or image.

Usage Example:

* Ingest a PDF:
  from src.visagent.file\_ingest import ingest\_file
  from src.rag\_node import RAGStore

  store = RAGStore(collection="visagent")
  metadata = {"uploaded\_by": "user\_1"}

  with open("example.pdf", "rb") as f:
  file\_bytes = f.read()

  ingest\_file(file\_bytes, "example.pdf", metadata, store)

* Ask a question:
  import requests

  response = requests.post(
  "[http://127.0.0.1:8000/ask](http://127.0.0.1:8000/ask)",
  json={"query": "Summarize the uploaded document"}
  )

  print(response.json())

Tech Stack:

* Python 3.10+
* FastAPI — Async API server
* LangGraph — Graph-based AI workflow
* Chroma DB — Vector database for RAG
* GroqLLM — Large language model backend
* Transformers — Pretrained embeddings
* PyPDF2 / Pillow — PDF and image processing

License:

* MIT License

Notes:

* Ensure your GroqLLM service is running or accessible; errors like '503 Service Unavailable' may occur during high load.
* Recommended to use a GPU for faster LLM inference if available.
* Keep 'models/' and 'data/' directories backed up if the project is restarted.

Author:

* Ayan Maity — M.Tech Student, CSE, IIT Kharagpur
