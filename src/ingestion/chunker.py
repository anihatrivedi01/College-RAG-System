from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    return chunks