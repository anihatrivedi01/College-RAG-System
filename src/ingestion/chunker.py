import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

# OCR chunks that hold a garbled table, replaced by clean chunks from data/processed/
SKIP_CHUNKS = {
    "regulation_for_unfair_means.pdf": range(13, 22),   # chunk ids 13 to 21
}

def clean_page_text(text):

    # Remove recurring Academic Council header
    text = re.sub(
        r"^.{0,10}Academic Council.{0,5}\n\W*13\.12\.2013\W*\n",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove footer containing IGDTU for Women
    text = re.sub(
        r"^.*IGDTU[\W_]*for[\W_]*Women.*$",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove "N | P a g e" footers (R&D guidelines)
    text = re.sub(
        r"(?m)^[ \t]*\d+[ \t]*\|[ \t]*P[ \t]*a[ \t]*g[ \t]*e[ \t]*$",
        "",
        text
    )
    
    # Remove lines containing only page numbers
    text = re.sub(
        r"^\s*\d{2,3}\s*$",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove obvious 1–2 character OCR junk lines
    text = re.sub(
        r"^\s*\S{1,2}\s*$",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove whitespace-only lines
    text = re.sub(
        r"(?m)^[ \t]+$",
        "",
        text
    )

    # Clean excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()

def chunk_text(pages, source):

    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150
    )

    all_chunks = []

    chunk_id = 0

    for page in pages:

        if "TABLE OF CONTENTS" in page["text"].upper():
            continue
        
        cleaned = clean_page_text(page["text"])

        page_chunks = splitter.split_text(cleaned)

        page_chunks = [
            c for c in page_chunks
            if len(c.strip()) > 100
        ]

        for chunk in page_chunks:

            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "source": source,
                    "page": page["page"],
                    "chunk_id": chunk_id
                }
            })

            chunk_id += 1

    skip = SKIP_CHUNKS.get(source, ())
    return [c for c in all_chunks if c["metadata"]["chunk_id"] not in skip]
            
        
    return all_chunks