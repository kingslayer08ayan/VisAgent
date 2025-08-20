import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma")
EMBED_MODEL  = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
DEVICE = "cpu"  # Force CPU for embeddings to reduce memory pressure
