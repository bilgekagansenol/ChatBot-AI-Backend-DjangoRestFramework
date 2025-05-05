# rag_engine/retriever.py
def get_rag_response(query: str) -> str:
    import pickle
    from sentence_transformers import SentenceTransformer, util

    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("rag_data/embeddings.pkl", "rb") as f:
        data = pickle.load(f)

    embeddings = data["embeddings"]
    metadata = data["metadata"]
    corpus = data["corpus"]

    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, embeddings)[0]
    top_result = int(cos_scores.argmax())

    return corpus[top_result]
