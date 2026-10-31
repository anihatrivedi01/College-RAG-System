import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SPLIT_PROMPT = """Split the user's question into separate, self-contained questions, one per distinct topic.
Rules:
- If the question asks about only one topic, return it unchanged as a list of one question.
- Each question must make sense on its own, without the others.
- Do not add new questions that the user did not ask.
- Return only a JSON list of strings.

Question: {question}"""


def split_question(question):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=SPLIT_PROMPT.format(question=question),
                config=types.GenerateContentConfig(
                    temperature=0,
                    response_mime_type="application/json",
                ),
            )
            parts = json.loads(response.text)
            if isinstance(parts, list) and parts and all(isinstance(p, str) for p in parts):
                return parts[:4]          # never more than 4 sub-questions
            break                         # reply was not a usable list
        except errors.APIError:
            time.sleep(10 * (attempt + 1))   # rate limit or server busy: wait, then retry
        except Exception:
            break                         # bad JSON or empty reply: no point retrying

    print("   [splitter fallback: using the original question]")
    return [question]