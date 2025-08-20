from src.nodes.rag_node import RAGStore
store = RAGStore()
store.add_document("LangGraph builds stateful agent workflows.", {"src": "note"})
print(store.query("What is LangGraph?", k=2))
