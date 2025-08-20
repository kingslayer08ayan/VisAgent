from typing import Dict, List
from src.llms.groqllm import GroqLLM

SYSTEM_PROMPT = """You are VisAgent, a precise multi-modal research assistant.
Answer with clear steps, cite retrieved snippets by index like [1], [2].
If an image caption is present, ground your reasoning to it.
"""

def _format_context(docs: List[str]) -> str:
    lines = []
    for i, d in enumerate(docs, 1):
        snippet = d.strip().replace("\n", " ")
        lines.append(f"[{i}] {snippet[:600]}")
    return "\n".join(lines)

def planner_and_responder(state: Dict, llm: GroqLLM):
    q = state.get("query", "")
    image_cap = state.get("vision_caption", None)
    docs = state.get("retrieved_docs", [])

    context = _format_context(docs) if docs else "No retrieved context."
    img_sec = f"\nImage caption: {image_cap}\n" if image_cap else ""

    prompt = f"""{SYSTEM_PROMPT}
Context:
{context}
{img_sec}
User question: {q}

Write a concise, well-structured answer with bullet points and a short final recommendation. Include citations like [1], [2] where relevant."""
    answer = llm.chat(prompt)
    state["answer"] = answer
    return state
