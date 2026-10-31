import json
import time
import sys

from google.genai import errors

from src.retrieval.retriever import retrieve_documents
from src.generation.context_builder import build_context
from src.generation.llm import generate_answer
from src.retrieval.retriever import retrieve_for_question

questions_file = sys.argv[1] if len(sys.argv) > 1 else "data/eval/questions.json"
tag = "hard" if "hard" in questions_file else "main"

with open(questions_file, encoding="utf-8") as f:
    questions = json.load(f)

def expected_sources(q):
    s = q["source"]
    if s is None:
        return []
    return s if isinstance(s, list) else [s]


results = []
def norm(text):
    return " ".join(text.lower().split())  

for q in questions:
    docs = retrieve_for_question(q["question"])     # uses the default k from retriever.py
    sources = expected_sources(q)
    must = q.get("must_contain", [])
    if must:
        hit = all(any(norm(m) in norm(d["text"]) for d in docs) for m in must)
    elif sources:
        hit = all(any(d["metadata"]["source"] == s for d in docs) for s in sources)
    else:
        hit = None

    missing = [m for m in must if not any(norm(m) in norm(d["text"]) for d in docs)]
    if missing:
        print(f"   Q{q['id']} missing phrases: {missing}")
    answer = None
    for attempt in range(4):
        try:
            answer = generate_answer(q["question"], build_context(docs))
            break
        except errors.APIError as e:
            wait = 15 * (attempt + 1)
            print(f"Q{q['id']}: Gemini error ({e.code}), retrying in {wait}s")
            time.sleep(wait)

    answer = answer or "[no answer returned]"

    no_answer_ok = None
    if q["expected"] == "NOT IN DOCUMENTS":
        no_answer_ok = "could not find" in answer.lower()

    results.append({
        "id": q["id"],
        "question": q["question"],
        "expected": q["expected"],
        "retrieval_hit": hit,
        "no_answer_ok": no_answer_ok,
        "retrieved": [
            f"{d['metadata']['source']} p{d['metadata']['page']} #{d['metadata']['chunk_id']}"
            for d in docs
        ],
        "answer": answer,
    })

    print(f"Q{q['id']} done (retrieval hit: {hit})")
    time.sleep(4)    # stay inside the free-tier rate limit

with open(f"data/eval/results_{tag}.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

with open(f"data/eval/results_{tag}.txt", "w", encoding="utf-8") as f:
    for r in results:
        f.write(f"Q{r['id']}: {r['question']}\n")
        f.write(f"EXPECTED: {r['expected']}\n")
        f.write(f"RETRIEVAL HIT: {r['retrieval_hit']}   RETRIEVED: {r['retrieved']}\n")
        f.write(f"ANSWER: {r['answer']}\n")
        f.write("-" * 70 + "\n")

answerable = [r for r in results if r["retrieval_hit"] is not None]
unanswerable = [r for r in results if r["no_answer_ok"] is not None]

print()
print(f"Retrieval hit: {sum(r['retrieval_hit'] for r in answerable)}/{len(answerable)}")
print(f"Correctly declined: {sum(r['no_answer_ok'] for r in unanswerable)}/{len(unanswerable)}")
print(f"Full answers saved to data/eval/results_{tag}.txt")