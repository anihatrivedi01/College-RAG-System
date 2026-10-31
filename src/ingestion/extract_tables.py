import json
import os
import time

import pymupdf
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from src.ingestion.table_jobs import TABLE_JOBS

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT = """These are consecutive pages of a university document. They contain a table: {describe}.
Return a JSON list with one object per table row, merging any row that continues across pages.
Use the table's column headings as keys (short, lowercase, underscores).
If a cell holds several items, use a list. {hint}
Do not include text that is not part of the table. Return only the JSON."""

os.makedirs("data/processed", exist_ok=True)

for job in TABLE_JOBS:
    out_path = f"data/processed/{job['name']}.json"

    # never overwrite a file you have already verified
    if os.path.exists(out_path):
        print(f"{job['name']}: already extracted, skipping")
        continue

    doc = pymupdf.open(job["pdf"])
    images = [
        types.Part.from_bytes(
            data=doc[p - 1].get_pixmap(dpi=200).tobytes("png"),
            mime_type="image/png",
        )
        for p in job["pages"]
    ]
    doc.close()

    prompt = PROMPT.format(describe=job["describe"], hint=job["hint"])

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
        except errors.ServerError:
            wait = 10 * (attempt + 1)
            print(f"{job['name']}: server busy, retrying in {wait}s (attempt {attempt + 1}/5)")
            time.sleep(wait)

    if response is None:
        print(f"{job['name']}: FAILED (server stayed unavailable)")
        continue

    if response.text is None:
        reason = response.candidates[0].finish_reason if response.candidates else "no candidates"
        print(f"{job['name']}: FAILED (no text returned, finish reason: {reason})")
        continue

    try:
        table = json.loads(response.text)
    except json.JSONDecodeError:
        print(f"{job['name']}: FAILED (reply was not valid JSON)")
        print(response.text)
        continue

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(table, f, indent=2, ensure_ascii=False)

    print(f"{job['name']}: saved {len(table)} rows")