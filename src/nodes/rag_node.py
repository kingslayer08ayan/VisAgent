from typing import Dict
from uuid import uuid4
import os
import chromadb
from src.utils.config import CHROMA_PATH
from src.utils.file_loader import (
    chunk_text,
    read_pdf_bytes_stream,
    read_text_file_bytes_stream
)
from src.utils.logging import get_logger
from sentence_transformers import SentenceTransformer

logger = get_logger("RAG")

class RAGStore:
    def __init__(self, collection: str = "visagent"):
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(BASE_DIR, "..", "..", "models", "all-MiniLM-L6-v2")
        logger.info(f"Loading local embedder from {model_dir} on CPU")
        self.embedder = SentenceTransformer(model_dir, device="cpu")

        self.col = self.client.get_or_create_collection(name=collection)
        logger.info(f"Chroma collection ready @ {CHROMA_PATH}")

    def add_document_stream(
        self,
        file_bytes: bytes,
        meta: Dict,
        file_type: str = "pdf",
        batch_size: int = 64
    ) -> int:
        """
        Memory-safe ingestion from raw file bytes.
        Supports 'pdf' or 'txt'.
        """
        if file_type.lower() == "pdf":
            chunk_iter = read_pdf_bytes_stream(file_bytes)
        else:
            chunk_iter = read_text_file_bytes_stream(file_bytes)

        total_chunks = 0
        batch, ids_batch = [], []

        for chunk in chunk_iter:
            batch.append(chunk)
            ids_batch.append(str(uuid4()))
            total_chunks += 1

            if len(batch) >= batch_size:
                embeddings = self.embedder.encode(batch, convert_to_numpy=True, normalize_embeddings=True)
                self.col.add(
                    documents=batch,
                    metadatas=[meta]*len(batch),
                    ids=ids_batch,
                    embeddings=embeddings.tolist()
                )
                del embeddings
                batch, ids_batch = [], []
                logger.info(f"Ingested {total_chunks} chunks so far")

        # Add any remaining chunks
        if batch:
            embeddings = self.embedder.encode(batch, convert_to_numpy=True, normalize_embeddings=True)
            self.col.add(
                documents=batch,
                metadatas=[meta]*len(batch),
                ids=ids_batch,
                embeddings=embeddings.tolist()
            )
            del embeddings

        logger.info(f"Finished ingestion: {total_chunks} chunks total")
        return total_chunks

    def query(self, q: str, k: int = 5) -> Dict:
        q_embedding = self.embedder.encode([q], convert_to_numpy=True, normalize_embeddings=True)[0]
        res = self.col.query(query_embeddings=[q_embedding], n_results=k)

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        ids  = res.get("ids", [[]])[0]
        return {"documents": docs, "metadatas": metas, "ids": ids}


def rag_node(state: Dict, store: RAGStore, top_k: int = 5) -> Dict:
    """
    Memory-safe retrieval node. 
    Retrieves top_k docs and only keeps what's needed in state.
    """
    q = state.get("query", "")
    if not q:
        state["retrieved_docs"] = []
        state["sources"] = []
        return state

    result = store.query(q, k=top_k)
    # Only keep top_k documents and their metadata
    state["retrieved_docs"] = result.get("documents", [])[:top_k]
    state["sources"] = result.get("metadatas", [])[:top_k]
    return state
