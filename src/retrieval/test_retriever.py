from src.retrieval.retriever import retrieve_documents


query = "What are the criteria for promotion to the next academic year?"

for n in [1, 2, 3, 4]:
    print(f"\n{'='*60}")
    print(f"n_results = {n}")
    print(f"{'='*60}")

    results = retrieve_documents(query, n_results=n)

    for i, result in enumerate(results):
        print(f"\n--- Result {i + 1} ---")
        print("Metadata:", result["metadata"])
        print("Text:", result["text"])