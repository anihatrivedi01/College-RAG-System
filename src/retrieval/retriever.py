from src.embeddings.embedder import create_embeddings
from src.retrieval.chroma_store import search_documents
from src.retrieval.query_splitter import split_question

def retrieve_for_question(query, n_results=3):
    sub_questions = split_question(query)

    seen = set()
    merged = []
    for sub in sub_questions:
        for doc in retrieve_documents(sub, n_results):
            key = (doc["metadata"]["source"], str(doc["metadata"]["chunk_id"]))
            if key not in seen:
                seen.add(key)
                merged.append(doc)

    return merged

def retrieve_documents(query, n_results=3):

    query_embedding = create_embeddings([query])

    results = search_documents(
        query_embedding,
        n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    retrieved = []

    for document, metadata in zip(documents, metadatas):

        retrieved.append({
            "text": document,
            "metadata": metadata
        })

    return retrieved