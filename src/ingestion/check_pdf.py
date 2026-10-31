import sys
from src.ingestion.document_loader import extract_text_from_pdf

if len(sys.argv) < 2:
    print("Usage: python -m src.ingestion.check_pdf <pdf_path> [page_number]")
    sys.exit(1)

pdf_path = sys.argv[1]
page_to_check = int(sys.argv[2]) if len(sys.argv) > 2 else None

pages = extract_text_from_pdf(pdf_path)

print("Number of pages extracted:", len(pages))

for p in pages:
    if page_to_check is None or p["page"] == page_to_check:
        print(f"\n--- Page {p['page']} ---")
        print(p["text"])