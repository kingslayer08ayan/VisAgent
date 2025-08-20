from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
from src.utils.file_loader import read_pdf_bytes, read_text_file_bytes
from src.utils.file_loader import image_from_bytes
from src.graphs.graph_builder import GraphBuilder

app = FastAPI(title="VisAgent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

gb = GraphBuilder()
graph = gb.build()

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    b = await file.read()
    meta = {"filename": file.filename, "type": file.content_type}
    if file.content_type in ["application/pdf", "application/x-pdf"]:
        text = read_pdf_bytes(b)
    elif file.content_type.startswith("text/"):
        text = read_text_file_bytes(b)
    else:
        return {"added_chunks": 0, "note": "Only PDF or text for ingestion."}
    n = await run_in_threadpool(gb.ingest_text, text, meta)
    return {"added_chunks": n, "meta": meta}

@app.post("/ask")
async def ask(query: str = Form(...), file: UploadFile | None = None):
    state = {"query": query}
    if file:
        if file.content_type.startswith("image/"):
            state["image_bytes"] = await file.read()
        elif file.content_type in ["application/pdf", "application/x-pdf", "text/plain"]:
            # quick one-shot context injection: ingest then ask
            b = await file.read()
            text = read_pdf_bytes(b) if "pdf" in file.content_type else read_text_file_bytes(b)
            await run_in_threadpool(gb.ingest_text, text, {"filename": file.filename})
    result = await run_in_threadpool(graph.invoke, state)
    return {"answer": result.get("answer", ""), "vision_caption": result.get("vision_caption", None)}
