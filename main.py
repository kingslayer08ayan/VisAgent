import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
from src.utils.file_loader import read_pdf_bytes, read_text_file_bytes, image_from_bytes
from src.nodes.rag_node import RAGStore
from src.graphs.graph_builder import GraphBuilder
from src.utils.logging import get_logger

logger = get_logger("VisAgent")

app = FastAPI(title="VisAgent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Initialize RAG store with GPU support if available
store = RAGStore(collection="visagent")
device = "cuda" if store.embedder.device.type == "cuda" else "cpu"
logger.info(f"Using device: {device.upper()}")

# Graph builder and graph instance
gb = GraphBuilder()
graph = gb.build()


@app.post("/ingest")
async def ingest(file: UploadFile = File(...), clear_existing: bool = Form(True)):
    b = await file.read()
    meta = {"filename": file.filename, "type": file.content_type}

    ext = os.path.splitext(file.filename)[1].lower()
    if ext == ".pdf":
        text = read_pdf_bytes(b)
        file_type = "pdf"
    elif ext == ".txt":
        text = read_text_file_bytes(b)
        file_type = "txt"
    else:
        return {"added_chunks": 0, "note": "Only PDF or text files supported."}

    # Ingest in threadpool
    added_chunks = await run_in_threadpool(
        store.add_document_stream,
        file_bytes=b,
        meta=meta,
        file_type=file_type,
        clear_existing=clear_existing
    )

    return {"added_chunks": added_chunks, "meta": meta}


@app.post("/ask")
async def ask(query: str = Form(...), file: UploadFile | None = None):
    state = {"query": query}

    # Optional one-shot ingestion for context
    if file:
        b = await file.read()
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in [".pdf", ".txt"]:
            await run_in_threadpool(
                store.add_document_stream,
                file_bytes=b,
                meta={"filename": file.filename},
                file_type="pdf" if ext == ".pdf" else "txt",
                clear_existing=False
            )
        elif ext in [".png", ".jpg", ".jpeg"]:
            state["image_bytes"] = b

    # Run graph invoke in threadpool
    result = await run_in_threadpool(graph.invoke, state)

    return {
        "answer": result.get("answer", ""),
        "vision_caption": result.get("vision_caption", None),
        "related_papers": result.get("related_papers", []),
        "new_research_ideas": result.get("new_research_ideas", [])
    }
