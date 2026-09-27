from src.embeddings.embedder import create_embeddings
from src.retrieval.chroma_store import search_documents


def retrieve_documents(query, n_results=2):
    query_embedding = create_embeddings([query])

    results = search_documents(
        query_embedding,
        n_results
    )

    return results["documents"][0]