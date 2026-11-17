
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# Resolve paths relative to the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "processed_chunks.jsonl"
)

VECTOR_STORE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vector_store"
    / "faiss_index"
)


def load_processed_chunks():
    """
    Read JSONL records and convert them into LangChain Documents.
    """

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Processed file not found: {INPUT_FILE}"
        )

    documents = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            try:
                record = json.loads(line)

                text = record.get("text", "").strip()

                if not text:
                    print(
                        f"Skipping empty record at line {line_number}"
                    )
                    continue

                metadata = {
                    "chunk_id": record.get("chunk_id", ""),
                    "source": record.get("source", "unknown"),
                    "page": record.get("page", "unknown")
                }

                documents.append(
                    Document(
                        page_content=text,
                        metadata=metadata
                    )
                )

            except json.JSONDecodeError as error:
                print(
                    f"Invalid JSON at line {line_number}: {error}"
                )

    if not documents:
        raise ValueError(
            "No valid text chunks found in processed_chunks.jsonl"
        )

    print(f"Loaded {len(documents)} document chunks.")

    return documents


def create_vector_store():

    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_actual_openai_api_key":
        raise ValueError(
            "OPENAI_API_KEY is missing. "
            "Check your project .env file."
        )

    embedding_model = os.getenv(
        "OPENAI_EMBEDDING_MODEL",
        "text-embedding-3-small"
    )

    print("\nLoading processed chunks...")

    documents = load_processed_chunks()

    print("\nInitializing OpenAI embeddings...")

    embeddings = OpenAIEmbeddings(
        model=embedding_model,
        api_key=api_key
    )

    print("\nGenerating embeddings and building FAISS index...")
    print("This step requires an internet connection.")

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    VECTOR_STORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vector_store.save_local(str(VECTOR_STORE_DIR))

    print("\nFAISS vector store created successfully!")
    print(f"Embedding model: {embedding_model}")
    print(f"Total vectors: {vector_store.index.ntotal}")
    print(f"Saved location: {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    create_vector_store()
