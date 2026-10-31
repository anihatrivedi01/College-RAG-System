from src.retrieval.chroma_store import collection


print("ChromaDB connected successfully.")
print("Collection name:", collection.name)
print("Number of stored documents:", collection.count())