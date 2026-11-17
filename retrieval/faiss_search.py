
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


PROJECT_ROOT = Path(__file__).resolve().parents[1]

VECTOR_STORE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vector_store"
    / "faiss_index"
)


def load_vector_store():

    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing from .env"
        )

    if not VECTOR_STORE_DIR.exists():
        raise FileNotFoundError(
            "FAISS index not found. "
            "Run create_vector_store.py first."
        )

    embedding_model = os.getenv(
        "OPENAI_EMBEDDING_MODEL",
        "text-embedding-3-small"
    )

    embeddings = OpenAIEmbeddings(
        model=embedding_model,
        api_key=api_key
    )

    # Only load an index that you created and trust locally.
    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


def search_documents(question, top_k=3):

    if not question.strip():
        raise ValueError("Please enter a question.")

    vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(
        question,
        k=top_k
    )

    print("\n" + "=" * 60)
    print("FARMING CHITTI - SEMANTIC SEARCH RESULTS")
    print("=" * 60)

    for rank, (document, distance) in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {rank}")
        print("-" * 40)

        print(f"Source: {document.metadata.get('source')}")
        print(f"Page: {document.metadata.get('page')}")
        print(f"Chunk ID: {document.metadata.get('chunk_id')}")

        # FAISS returns an L2 distance here, not a probability.
        print(f"Vector distance: {distance:.4f}")

        print("\nExtracted content:")
        print(document.page_content[:1000])

    return results


if __name__ == "__main__":

    user_question = input(
        "\nAsk Farming Chitti a question: "
    )

    search_documents(user_question, top_k=3)
