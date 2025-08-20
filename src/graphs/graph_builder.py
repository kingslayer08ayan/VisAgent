from typing import TypedDict, Dict, Any, Union
from langgraph.graph import StateGraph, END
from src.nodes.rag_node import RAGStore, rag_node
from src.nodes.vision_node import Vision, vision_node
from src.nodes.response_node import planner_and_responder
from src.llms.groqllm import GroqLLM

class AgentState(TypedDict, total=False):
    query: str
    image_bytes: bytes
    vision_caption: str
    retrieved_docs: list
    sources: list
    answer: str

class GraphBuilder:
    def __init__(self):
        self.store = RAGStore()
        self.vision = Vision()
        self.llm = GroqLLM()

    # universal ingestion: str or bytes
    def ingest_text(self, content: Union[str, bytes], meta: Dict[str, Any], file_type: str = "txt"):
        """
        content: str (plain text) or bytes (PDF/TXT)
        file_type: "txt" or "pdf"
        """
        if isinstance(content, str):
            content = content.encode("utf-8")  # convert string to bytes
            file_type = "txt"  # override file type

        return self.store.add_document_stream(
            file_bytes=content,
            meta=meta,
            file_type=file_type,
            batch_size=64
        )

    def build(self):
        g = StateGraph(AgentState)

        def _vision(state: AgentState): return vision_node(state, self.vision)
        def _rag(state: AgentState):    return rag_node(state, self.store)
        def _solve(state: AgentState):  return planner_and_responder(state, self.llm)

        g.add_node("vision", _vision)
        g.add_node("rag", _rag)
        g.add_node("solve", _solve)

        g.set_entry_point("vision")
        g.add_edge("vision", "rag")
        g.add_edge("rag", "solve")
        g.add_edge("solve", END)

        return g.compile()
