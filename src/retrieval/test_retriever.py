from src.retrieval.retriever import retrieve_documents


query = "What are the criteria for promotion to the next academic year?"

documents = retrieve_documents(query, n_results=2)

print("===== RETRIEVED DOCUMENTS =====")

for i, document in enumerate(documents):
    print(f"\nDocument {i + 1}:")
    print(document)