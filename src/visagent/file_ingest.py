import os
from src.utils.file_loader import (
    read_pdf_bytes_stream,
    read_text_file_bytes_stream,
    image_from_bytes
)
from src.nodes.rag_node import RAGStore
from src.utils.logging import get_logger

logger = get_logger("VisAgent")

def ingest_file(file_bytes: bytes, filename: str, metadata: dict, store: RAGStore, batch_size: int = 64):
    """
    Memory-safe ingestion of a user-uploaded file into RAGStore.
    Supports PDF and TXT files. Images can be handled separately if needed.
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext in [".pdf", ".txt"]:
        file_type = "pdf" if ext == ".pdf" else "txt"
        total_chunks = store.add_document_stream(
            file_bytes=file_bytes,
            meta=metadata,
            file_type=file_type,
            batch_size=batch_size
        )
        logger.info(f"Ingested {total_chunks} chunks from {filename}")

    elif ext in [".png", ".jpg", ".jpeg"]:
        img = image_from_bytes(file_bytes)
        metadata["filename"] = filename
        # Optionally, store image metadata or features in RAG if needed
        logger.info(f"Image {filename} processed (not chunked)")

    else:
        logger.warning(f"Unsupported file type: {filename}")

    return True
