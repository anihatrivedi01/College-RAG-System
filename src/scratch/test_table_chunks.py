from src.ingestion.table_chunks import load_table_chunks, load_manual_chunks

chunks = load_table_chunks() + load_manual_chunks()

print("Total table/manual chunks:", len(chunks))

for c in chunks:
    print("\n", c["metadata"], "-", len(c["text"]), "characters")
    print(c["text"])