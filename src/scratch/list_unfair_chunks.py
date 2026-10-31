from src.ingestion.document_loader import extract_text_from_pdf
from src.ingestion.chunker import chunk_text

pages = extract_text_from_pdf("data/raw/regulation_for_unfair_means.pdf")
chunks = chunk_text(pages, source="regulation_for_unfair_means.pdf")

for c in chunks:
    if 5 <= c["metadata"]["page"] <= 8:
        print(c["metadata"]["page"], c["metadata"]["chunk_id"], "|", c["text"][:90].replace("\n", " "))