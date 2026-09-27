from src.retrieval.retriever import retrieve_documents
from src.generation.llm import generate_answer


query = "What are the criteria for promotion to the next academic year?"

documents = retrieve_documents(query, n_results=2)

context = "\n\n".join(documents)

print("===== RETRIEVED CONTEXT =====")
print(context)

answer = generate_answer(query, context)

print("\n===== FINAL ANSWER =====")
print(answer)