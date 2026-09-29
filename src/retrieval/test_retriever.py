from src.retrieval.retriever import retrieve_documents

questions = [
    "What are the criteria for promotion to the next academic year?",
    "What is the punishment for carrying a mobile phone into the exam?",
    "What financial assistance is available for Ph.D scholars?",
    "How much extra time is given to a disabled student with a scribe?",
]

for q in questions:
    print(f"\n=== {q} ===")
    results = retrieve_documents(q, n_results=3)
    for r in results:
        print(f"- {r['metadata']['source']} (page {r['metadata']['page']}): {r['text'][:100]}")