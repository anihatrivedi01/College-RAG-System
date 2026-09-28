import os
import sys

from src.ingestion.document_loader import extract_text_from_pdf
from src.ingestion.chunker import chunk_text


pdf_path = sys.argv[1]

source = os.path.basename(pdf_path)

pages = extract_text_from_pdf(pdf_path)

chunks = chunk_text(
    pages,
    source=source
)

print("Number of pages:", len(pages))
print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):

    print(f"\n===== CHUNK {i+1} =====")

    print("Metadata:")
    print(chunk["metadata"])

    print("\nText preview:")
    print(chunk["text"][:300])

    if i < len(chunks) - 1:

        print("\n--- OVERLAP CHECK ---")
        print("End of current chunk:")
        print(chunk["text"][-150:])

        print("\nStart of next chunk:")
        print(chunks[i + 1]["text"][:150])
        