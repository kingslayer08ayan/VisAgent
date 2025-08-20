import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("VisAgent • Multi-Modal RAG (Groq + LangGraph)")
st.caption("Upload a PDF/text/image and ask a question. Uses Groq for reasoning, Chroma for RAG.")

with st.sidebar:
    st.write("Backend:", BACKEND)
    up_file = st.file_uploader("Optional: Upload PDF/Text/Image", type=["pdf", "txt", "png", "jpg", "jpeg"])
    if up_file is not None and st.button("Ingest (PDF/TXT)"):
        files = {"file": (up_file.name, up_file.getvalue(), up_file.type)}
        try:
            r = requests.post(f"{BACKEND}/ingest", files=files, timeout=120)
            r.raise_for_status()
            st.success(r.json())
        except Exception as e:
            st.error(f"Ingest failed: {e}")

q = st.text_input("Your question")
go = st.button("Ask")

if go and q:
    files = None
    if up_file is not None and up_file.type.startswith("image/"):
        files = {"file": (up_file.name, up_file.getvalue(), up_file.type)}
    data = {"query": q}
    try:
        r = requests.post(f"{BACKEND}/ask", data=data, files=files, timeout=600)
        r.raise_for_status()
        res = r.json()
        if res.get("vision_caption"):
            st.info(f"Image caption: {res['vision_caption']}")
        st.markdown(res.get("answer", ""))
    except Exception as e:
        st.error(f"Query failed: {e}")
