import os
from dotenv import load_dotenv
from google import genai


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
3. If the answer cannot be found in the context, say:
   "I could not find this information in the provided college documents."
4. After answering, provide the source and page number from the context.
5. Keep the answer concise and clear.

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text