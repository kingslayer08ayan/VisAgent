from src.graphs.graph_builder import GraphBuilder
gb = GraphBuilder()
gb.ingest_text("BLIP is for image captioning.", {"src":"note"})
g = gb.build()
out = g.invoke({"query":"What is BLIP?"})
print(out["answer"][:200])
