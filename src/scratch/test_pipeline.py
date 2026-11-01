from src.pipeline import answer_question

for q in [
    "What is the weightage of the end-term examination for theory courses?",
    "What is the hostel fee for first-year students?",
]:
    result = answer_question(q)
    print("\nQ:", q)
    print("A:", result["answer"])
    print("Sources:", [(s["source"], s["page"]) for s in result["sources"]])