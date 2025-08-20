# VisAgent

## Overview

VisAgent is an advanced multi-modal AI agent integrating vision, RAG, and LLM capabilities. It supports document ingestion, image understanding, and context-aware question answering.

## Features

* Multi-Modal Ingestion: PDFs, images, text
* Vision Understanding
* RAG-Based Retrieval
* LLM Integration with GroqLLM
* FastAPI Backend

## Architecture

* **RAGStore**: Document ingestion & retrieval
* **Vision Module**: Image processing
* **GroqLLM**: Language understanding & generation
* **StateGraph**: Workflow orchestration

## Installation

```bash
git clone https://github.com/kingslayer08ayan/VisAgent.git
cd VisAgent
conda create -n visagent python=3.10
conda activate visagent
pip install -r requirements.txt
```

Download required models to `./models/`:

* all-MiniLM-L6-v2
* GroqLLM weights

## Usage

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

Endpoints:

* `POST /ingest`: Upload document for processing
* `POST /ask`: Submit a question or image

## Project Structure

```
VisAgent/
├─ src/
│  ├─ llms/
│  ├─ nodes/
│  ├─ graphs/
│  └─ utils/
├─ models/
├─ main.py
├─ requirements.txt
└─ README.md
```

## Contributing

1. Fork the repo
2. Create feature branch
3. Commit changes
4. Push branch
5. Open PR

## License

MIT License

## Contact
GitHub: kingslayer08ayan 
Email: ayanmaity874@gmail.com
GitHub: [kingslayer08ayan](https://github.com/kingslayer08ayan)
Email: [your.email@example.com](mailto:your.email@example.com)
