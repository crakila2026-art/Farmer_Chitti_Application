
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents,
    chunk_size=1000,
    chunk_overlap=200
):
    """
    Split page-level documents into smaller chunks.

    Each chunk retains its source PDF and page number.
    """

    if not documents:
        raise ValueError("No documents received for chunking.")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative "
            "and smaller than chunk_size."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    # Assign a sequential chunk ID and preserve metadata.
    for index, chunk in enumerate(chunks, start=1):

        chunk.metadata["chunk_id"] = f"chunk_{index:06d}"

        # Keep the page number and source for citations.
        chunk.metadata["source"] = chunk.metadata.get(
            "source", "unknown"
        )

        chunk.metadata["page"] = chunk.metadata.get(
            "page", "unknown"
        )

    print("\nChunking completed.")
    print(f"Total chunks created: {len(chunks)}")

    return chunks


if __name__ == "__main__":
    from pdf_loader import load_pdf_documents

    documents = load_pdf_documents()
    chunks = split_documents(documents)

    print("\nSample chunk:")
    print(chunks[0].page_content[:500])

    print("\nSample chunk metadata:")
    print(chunks[0].metadata)
