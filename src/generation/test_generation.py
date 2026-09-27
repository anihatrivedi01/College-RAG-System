from src.generation.llm import generate_answer


query = "What are the criteria for promotion to the next academic year?"

context = """
A student will be promoted to the next academic year only if the student
has obtained at least 50% of the total credits of the ensuing academic year
and 90% of the total credits of the previous year, excluding the credits
of the ensuing academic year.
"""


answer = generate_answer(query, context)

print("===== GENERATED ANSWER =====")
print(answer)