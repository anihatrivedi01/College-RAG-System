import chromadb


client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="college_documents"
)


def add_documents(chunks, embeddings, ids):
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )


def search_documents(query_embedding, n_results=2):
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )

    return results