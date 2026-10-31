from src.ingestion.document_loader import extract_text_from_pdf
from src.ingestion.chunker import chunk_text
from src.embeddings.embedder import create_embeddings


pdf_path = "data/raw/criteria_for_passing_exams.pdf"

# Extract pages
pages = extract_text_from_pdf(pdf_path)

# Create chunks with metadata
chunks = chunk_text(
    pages,
    source="criteria_for_passing_exams.pdf"
)

# Extract only text for embedding
texts = [chunk["text"] for chunk in chunks]

# Create embeddings
embeddings = create_embeddings(texts)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))

print("\nFirst chunk:")
print(chunks[0])

print("\nFirst embedding:")
print(embeddings[0][:10])