import json
import os
import sys

import pymupdf
from dotenv import load_dotenv
from google import genai
from google.genai import types

import time
from google.genai import errors

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

pdf_path = sys.argv[1]
pages = [int(p) for p in sys.argv[2:]]

doc = pymupdf.open(pdf_path)
images = [
    types.Part.from_bytes(
        data=doc[p - 1].get_pixmap(dpi=200).tobytes("png"),
        mime_type="image/png",
    )
    for p in pages
]
doc.close()

prompt = """These are consecutive pages of a university regulation containing a table
of offences and punishments. A table row can continue from one page to the next.
Return a JSON list with one item per Part (A, B, C, ...), merging any row that
continues across pages. Each item has:
"part": the letter in the first column,
"offences": a list of every offence in that Part, each in concise words, keeping
any conditions (for example "and the candidate made actual use of the material"),
"punishment": the full punishment text, including any durations in months.
Return only the JSON."""

response = None
for attempt in range(5):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[prompt] + images,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
            ),
        )
        break
    except errors.ServerError as e:
        wait = 10 * (attempt + 1)
        print(f"Server busy ({e.code}), retrying in {wait}s... (attempt {attempt + 1}/5)")
        time.sleep(wait)

if response is None:
    raise SystemExit("Gemini stayed unavailable after 5 attempts. Try again later.")

if response.candidates:
    print("Finish reason:", response.candidates[0].finish_reason)

if response.text is None:
    raise SystemExit("Gemini returned no text (see finish reason above).")

table = json.loads(response.text)  # fails loudly if the output is not valid JSON

print(json.dumps(table, indent=2, ensure_ascii=False))

os.makedirs("data/processed", exist_ok=True)
with open("data/processed/unfair_means_table.json", "w", encoding="utf-8") as f:
    json.dump(table, f, indent=2, ensure_ascii=False)

print("\nSaved to data/processed/unfair_means_table.json")