import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_answer(query, context):

    prompt = f"""
You are a college assistant.

Answer the user's question using ONLY the information provided
in the context below.

Rules:
1. Do not use information that is not present in the context.
2. Do not make up or assume information.
3. If the answer cannot be found in the context, reply with exactly this sentence
   and nothing else, with no source and no extra text:
   "I could not find this information in the provided college documents."
4. Otherwise, after answering, provide the source and page number from the context.
5. Answer the question directly and completely. Include every condition, limit,
   amount and exception that the context states about what was asked.
   Do not add details about unrelated topics.
6. The context may contain OCR errors or text that is cut off in the middle of a sentence.
   Do not guess or complete missing words. If a rule seems incomplete,
   say that the text appears incomplete.
7. If the context describes several cases with different outcomes (for example,
   different penalties depending on the circumstances), state each case separately.
8. Write numbers and fractions in plain text (for example 1/3), without LaTeX
   or special symbols.

Context:
{context}

Question:
{query}

"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2)
    )

    return response.text