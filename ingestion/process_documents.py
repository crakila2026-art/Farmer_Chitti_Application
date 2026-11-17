
import json
import hashlib
from pathlib import Path

from ingestion.pdf_loader import load_pdf_documents
from ingestion.chunking import split_documents


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_FOLDER / "processed_chunks.jsonl"


def generate_chunk_id(source, page, chunk_index, content):
    """
    Generate a reproducible ID for a chunk.
    """
    unique_text = (
        f"{source}|{page}|{chunk_index}|{content}"
    )

    return hashlib.sha256(
        unique_text.encode("utf-8")
    ).hexdigest()[:16]


def save_chunks(chunks, output_file=OUTPUT_FILE):

    output_file = Path(output_file)
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        for index, chunk in enumerate(chunks, start=1):

            source = chunk.metadata.get(
                "source", "unknown"
            )

            page = chunk.metadata.get(
                "page", "unknown"
            )

            chunk_id = generate_chunk_id(
                source,
                page,
                index,
                chunk.page_content
            )

            record = {
                "chunk_id": chunk_id,
                "source": source,
                "page": page,
                "text": chunk.page_content
            }

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    print(f"\nProcessed chunks saved to:")
    print(output_file)


def main():

    print("=" * 50)
    print("FARMING CHITTI - PDF PROCESSING")
    print("=" * 50)

    # Step 1: Extract PDF text
    documents = load_pdf_documents()

    # Step 2: Split text into chunks
    chunks = split_documents(
        documents,
        chunk_size=1000,
        chunk_overlap=200
    )

    # Step 3: Save chunks
    save_chunks(chunks)

    print("\nProcessing summary")
    print("-" * 30)
    print(f"Total pages: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nPhase 2 completed successfully!")


if __name__ == "__main__":
    main()
