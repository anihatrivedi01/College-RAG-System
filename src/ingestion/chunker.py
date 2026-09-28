from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(pages, source):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150
    )

    chunk_data = []

    chunk_id = 0

    for page in pages:

        chunks = splitter.split_text(page["text"])

        for chunk in chunks:

            chunk_data.append({
                "text": chunk,
                "metadata": {
                    "source": source,
                    "page": page["page"],
                    "chunk_id": chunk_id
                }
            })

            chunk_id += 1

    return chunk_data