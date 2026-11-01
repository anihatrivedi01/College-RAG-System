from src.retrieval.retriever import retrieve_for_question
from src.generation.context_builder import build_context
from src.generation.llm import generate_answer


def answer_question(question):
    docs = retrieve_for_question(question)
    answer = generate_answer(question, build_context(docs))

    declined = "could not find this information" in answer.lower()

    # no sources are shown when the system declines to answer
    sources = []
    seen = set()
    if not declined:
        for d in docs:
            key = (d["metadata"]["source"], str(d["metadata"]["page"]))
            if key in seen:
                continue
            seen.add(key)
            sources.append({
                "source": key[0],
                "page": key[1],
                "snippet": d["text"][:200],
            })

    return {"answer": answer, "sources": sources}