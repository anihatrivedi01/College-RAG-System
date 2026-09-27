from src.ingestion.document_loader import extract_text_from_pdf
from src.ingestion.chunker import chunk_text

pdf_path = "data/raw/criteria_for_passing_exams.pdf"

text = extract_text_from_pdf(pdf_path)
chunks = chunk_text(text)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n===== CHUNK {i+1} =====")
    print(chunk)

    if i < len(chunks) - 1:
        print("\n--- END OF THIS CHUNK ---")
        print(chunk[-200:])
        print("\n--- START OF NEXT CHUNK ---")
        print(chunks[i+1][:200])