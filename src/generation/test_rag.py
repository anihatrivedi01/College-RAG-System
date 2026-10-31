from src.retrieval.retriever import retrieve_documents
from src.generation.llm import generate_answer


query = query = "How much extra time is given to a disabled student with a scribe?"

documents = retrieve_documents(query, n_results=3)


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