from typing import List, Iterator
from io import BytesIO
from PIL import Image
from pypdf import PdfReader

def read_pdf_bytes_stream(pdf_bytes: bytes, chunk_size: int = 1000) -> Iterator[str]:
    """
    Yield text chunks from a PDF without loading the entire file into memory.
    """
    reader = PdfReader(BytesIO(pdf_bytes))
    buffer = ""
    for page in reader.pages:
        txt = page.extract_text() or ""
        buffer += txt + "\n"

        # Yield chunks from buffer
        while len(buffer) >= chunk_size:
            yield buffer[:chunk_size]
            buffer = buffer[chunk_size:]

    if buffer.strip():
        yield buffer.strip()


def read_text_file_bytes_stream(b: bytes, chunk_size: int = 1000) -> Iterator[str]:
    """
    Yield text chunks from a text file without loading the entire text into memory.
    """
    try:
        text = b.decode("utf-8")
    except:
        text = b.decode("latin-1", errors="ignore")

    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        yield text[start:end].strip()
        start = end


def read_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Legacy function: reads entire PDF into memory (keep for small files)
    """
    reader = PdfReader(BytesIO(pdf_bytes))
    chunks = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        chunks.append(txt)
    return "\n".join(chunks)


def read_text_file_bytes(b: bytes) -> str:
    """
    Legacy function: reads entire text file into memory (keep for small files)
    """
    try:
        return b.decode("utf-8")
    except:
        return b.decode("latin-1", errors="ignore")


def image_from_bytes(b: bytes) -> Image.Image:
    return Image.open(BytesIO(b)).convert("RGB")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks with overlap. Works for in-memory strings.
    """
    text = text.replace("\r", " ")
    res, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        res.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return [c.strip() for c in res if c.strip()]
