VisAgent
========

Overview:
---------
VisAgent is an advanced multi-modal AI agent that integrates vision, retrieval-augmented generation (RAG),
and large language model (LLM) capabilities. It supports intelligent document ingestion, image understanding,
and context-aware question answering for research, enterprise knowledge bases, and personal assistant applications.

Features:
---------
- Multi-Modal Ingestion: Upload and process PDFs, images, and text files.
- Vision Understanding: Analyze and interpret images using state-of-the-art vision models.
- RAG-Based Retrieval: Efficiently retrieve relevant information from a local vector store.
- LLM Integration: Generate context-aware responses using GroqLLM.
- FastAPI Backend: Lightweight and scalable API for integration.

Architecture:
-------------
- RAGStore: Manages document ingestion and retrieval.
- Vision Module: Processes and understands visual inputs.
- GroqLLM: Provides advanced language understanding and generation.
- StateGraph: Orchestrates workflow between components.

Installation:
-------------
Prerequisites:
  - Python 3.10+
  - Conda (for environment management)

Steps:
1. Clone the repository:
   git clone https://github.com/kingslayer08ayan/VisAgent.git
   cd VisAgent

2. Create and activate a virtual environment:
   conda create -n visagent python=3.10
   conda activate visagent

3. Install dependencies:
   pip install -r requirements.txt

4. Download necessary models to ./models/
   - all-MiniLM-L6-v2 (for embeddings)
   - GroqLLM weights (for language processing)

Usage:
------
Start the FastAPI server:
  uvicorn main:app --reload --port 8000

API Endpoints:
  - POST /ingest : Upload a document (PDF, TXT, or image) for processing.
  - POST /ask    : Submit a question or image to receive an intelligent response.

Project Structure:
------------------
VisAgent/
  src/            # Core source code
    llms/         # LLM wrappers (e.g., GroqLLM)
    nodes/        # Vision, RAG, and response nodes
    graphs/       # GraphBuilder for agent orchestration
    utils/        # Utility functions and helpers
  models/         # Pre-trained models and weights
  assets/         # Project assets (logos, diagrams)
  main.py         # FastAPI application entry point
  requirements.txt# Python dependencies
  README.txt      # Project documentation

Contributing:
-------------
1. Fork the repository.
2. Create a feature branch:
   git checkout -b feature/YourFeature
3. Commit your changes:
   git commit -m 'Add new feature'
4. Push to the branch:
   git push origin feature/YourFeature
5. Open a pull request describing your changes.

License:
--------
This project is licensed under the MIT License. See the LICENSE file for details.

Contact:
--------
GitHub: https://github.com/kingslayer08ayan
Email: ayanmaity874@gmail.com
