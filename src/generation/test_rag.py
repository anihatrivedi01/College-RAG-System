from src.retrieval.retriever import retrieve_documents
from src.generation.llm import generate_answer


query = "What are the criteria for promotion to the next academic year?"

documents = retrieve_documents(query, n_results=2)


# Build context for the LLM
context_parts = []

for document in documents:

    metadata = document["metadata"]
    text = document["text"]

    context_parts.append(
        f"""SOURCE: {metadata['source']}
PAGE: {metadata['page']}
CHUNK: {metadata['chunk_id']}

{text}"""
    )


context = "\n\n---\n\n".join(context_parts)


print("===== RETRIEVED CONTEXT =====")
print(context)


answer = generate_answer(query, context)


print("\n===== FINAL ANSWER =====")
print(answer)