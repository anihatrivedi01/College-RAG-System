from src.ingestion.document_loader import extract_text_from_pdf

pdf_path = "data/raw/conduct_and_evaluation_of_examinations.pdf"

pages = extract_text_from_pdf(pdf_path)

print("Number of pages extracted:", len(pages))

# Look at one page you can verify against the real PDF
page_to_check = 7

for p in pages:
    if p["page"] == page_to_check:
        print(f"\n--- Page {page_to_check} ---")
        print(p["text"])