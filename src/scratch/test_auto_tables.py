import os
import sys

from src.ingestion.auto_tables import extract_tables_from_pdf

pdf_path = sys.argv[1]
report = []

chunks = extract_tables_from_pdf(pdf_path, source=os.path.basename(pdf_path), report=report)

print("Candidate tables:")
for line in report:
    print("  ", line)

print("\nTable chunks:", len(chunks))
for c in chunks[:8]:                       # show the first 8 only
    print("\n", c["metadata"]["chunk_id"])
    print(c["text"])