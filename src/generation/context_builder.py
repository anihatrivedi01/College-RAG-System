def build_context(retrieved_documents):

    context_parts = []

    for result in retrieved_documents:

        metadata = result["metadata"]
        text = result["text"]

        context_parts.append(
            f"""SOURCE: {metadata['source']}
PAGE: {metadata['page']}
CHUNK: {metadata['chunk_id']}

{text}"""
        )

    return "\n\n---\n\n".join(context_parts)