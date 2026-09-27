import chromadb
from src.ingestion.document_loader import extract_text_from_pdf
from src.ingestion.chunker import chunk_text
from src.embeddings.embedder import create_embeddings


# 1. Load PDF
pdf_path = "data/raw/criteria_for_passing_exams.pdf"

text = extract_text_from_pdf(pdf_path)


# 2. Create chunks
chunks = chunk_text(text)

print("Number of chunks:", len(chunks))


# 3. Create embeddings
embeddings = create_embeddings(chunks)

print("Number of embeddings:", len(embeddings))


# 4. Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="college_documents"
)


# 5. Create IDs
ids = [f"criteria_chunk_{i}" for i in range(len(chunks))]


# 6. Store chunks + embeddings
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings.tolist()
)

print("Documents added to ChromaDB.")


# 7. Test semantic search
query = "What are the criteria for promotion to the next academic year?"

query_embedding = create_embeddings([query])

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=2
)


print("\n===== SEARCH RESULTS =====")

for i, document in enumerate(results["documents"][0]):
    print(f"\nResult {i + 1}:")
    print(document)