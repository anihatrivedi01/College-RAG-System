
print("INGEST SCRIPT STARTED")
import os
from src.ingestion.document_loader import extract_text_from_pdf
from src.ingestion.chunker import chunk_text
from src.embeddings.embedder import create_embeddings
from src.retrieval.chroma_store import add_documents, collection
from src.ingestion.table_chunks import load_table_chunks, load_manual_chunks

existing = collection.get()["ids"]
if existing:
    collection.delete(ids=existing)
print("Collection cleared. Starting from", collection.count(), "chunks")


raw_dir = "data/raw"

for filename in sorted(os.listdir(raw_dir)):
    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(raw_dir, filename)
    pages = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(pages, source=filename)

    texts = [c["text"] for c in chunks]
    embeddings = create_embeddings(texts)

    ids = [
        f"{c['metadata']['source']}_{c['metadata']['page']}_{c['metadata']['chunk_id']}"
        for c in chunks
    ]

    add_documents(chunks, embeddings, ids)
    print(f"{filename}: {len(pages)} pages, {len(chunks)} chunks")

    

extra = load_table_chunks() + load_manual_chunks()
extra_embeddings = create_embeddings([c["text"] for c in extra])
extra_ids = [f"{c['metadata']['source']}_{c['metadata']['chunk_id']}" for c in extra]
add_documents(extra, extra_embeddings, extra_ids)
print(f"table/manual chunks: {len(extra)} added")

print("\nTotal chunks in collection:", collection.count())