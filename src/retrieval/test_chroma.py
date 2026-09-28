from src.ingestion.document_loader import extract_text_from_pdf
from src.ingestion.chunker import chunk_text
from src.embeddings.embedder import create_embeddings
from src.retrieval.chroma_store import add_documents, collection


# 1. Load PDF
pdf_path = "data/raw/criteria_for_passing_exams.pdf"

pages = extract_text_from_pdf(pdf_path)


# 2. Create chunks with metadata
chunks = chunk_text(
    pages,
    source="criteria_for_passing_exams.pdf"
)

print("Number of chunks:", len(chunks))


# 3. Extract only text for embeddings
texts = [chunk["text"] for chunk in chunks]

embeddings = create_embeddings(texts)

print("Number of embeddings:", len(embeddings))


# 4. Create IDs
ids = [
    f"{chunk['metadata']['source']}_{chunk['metadata']['page']}_{chunk['metadata']['chunk_id']}"
    for chunk in chunks
]


# 5. Store chunks + embeddings + metadata
add_documents(
    chunks,
    embeddings,
    ids
)

print("Documents added to ChromaDB.")


# 6. Test semantic search
query = "What are the criteria for promotion to the next academic year?"

query_embedding = create_embeddings([query])[0]


results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2
)


print("\n===== SEARCH RESULTS =====")

for i, document in enumerate(results["documents"][0]):

    print(f"\nResult {i + 1}:")

    print("Metadata:")
    print(results["metadatas"][0][i])

    print("\nDocument:")
    print(document)