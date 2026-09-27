from src.ingestion.document_loader import extract_text_from_pdf
from src.ingestion.chunker import chunk_text
from src.embeddings.embedder import create_embeddings


pdf_path = "data/raw/criteria_for_passing_exams.pdf"

# Extract text
text = extract_text_from_pdf(pdf_path)

# Create chunks
chunks = chunk_text(text)

# Create embeddings
embeddings = create_embeddings(chunks)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))

print("\nFirst chunk:")
print(chunks[0])

print("\nFirst embedding:")
print(embeddings[0][:10])