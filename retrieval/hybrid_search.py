
import json
import re
from pathlib import Path
from collections import defaultdict

from rank_bm25 import BM25Okapi
from langchain_core.documents import Document

from retrieval.faiss_search import load_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "processed_chunks.jsonl"
)

# Number of candidates collected from each search engine
CANDIDATE_K = 10

# Number of final results returned
FINAL_K = 5

# RRF ranking constant
RRF_K = 60


def tokenize(text):
    """
    Basic Unicode-aware tokenizer.

    Supports whitespace-separated words and retains
    tokens from Indian language scripts.
    """

    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def load_bm25_documents():
    """
    Load processed JSONL chunks and create BM25 index.
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
                    continue

                document = Document(
                    page_content=text,
                    metadata={
                        "chunk_id": record.get("chunk_id", ""),
                        "source": record.get("source", "unknown"),
                        "page": record.get("page", "unknown")
                    }
                )

                documents.append(document)

            except json.JSONDecodeError as error:
                print(
                    f"Skipping invalid JSON at line "
                    f"{line_number}: {error}"
                )

    if not documents:
        raise ValueError("No documents available for BM25.")

    return documents


def create_bm25_index(documents):
    """
    Create BM25 keyword search index.
    """

    tokenized_corpus = [
        tokenize(document.page_content)
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    return bm25


def get_document_key(document):
    """
    Use chunk_id to identify the same chunk across
    FAISS and BM25. Fall back to a content-based key.
    """

    chunk_id = document.metadata.get("chunk_id")

    if chunk_id:
        return str(chunk_id)

    return (
        str(document.metadata.get("source", "unknown"))
        + "|"
        + str(document.metadata.get("page", "unknown"))
        + "|"
        + document.page_content
    )


def reciprocal_rank_fusion(
    faiss_results,
    bm25_results,
    rrf_k=RRF_K
):
    """
    Combine FAISS and BM25 rankings using RRF.

    Both systems contribute one reciprocal-rank score
    for every chunk they retrieve.
    """

    fused_scores = defaultdict(float)
    documents = {}

    # Process FAISS rankings
    for rank, document in enumerate(faiss_results, start=1):

        key = get_document_key(document)

        fused_scores[key] += 1 / (rrf_k + rank)
        documents[key] = document

    # Process BM25 rankings
    for rank, document in enumerate(bm25_results, start=1):

        key = get_document_key(document)

        fused_scores[key] += 1 / (rrf_k + rank)
        documents[key] = document

    ranked_results = sorted(
        fused_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        {
            "document": documents[key],
            "rrf_score": score
        }
        for key, score in ranked_results
    ]


def hybrid_search(
    question,
    candidate_k=CANDIDATE_K,
    final_k=FINAL_K
):
    """
    Execute semantic search, keyword search,
    and Reciprocal Rank Fusion.
    """

    if not question or not question.strip():
        raise ValueError("Please enter a valid question.")

    print("\nLoading BM25 documents...")

    bm25_documents = load_bm25_documents()

    print(f"BM25 document count: {len(bm25_documents)}")

    print("\nCreating BM25 index...")

    bm25 = create_bm25_index(bm25_documents)

    print("\nLoading FAISS vector database...")

    vector_store = load_vector_store()

    # ------------------------------------------------
    # 1. FAISS semantic search
    # ------------------------------------------------

    print("\nRunning FAISS semantic search...")

    faiss_results = vector_store.similarity_search(
        question,
        k=min(candidate_k, vector_store.index.ntotal)
    )

    print(f"FAISS results: {len(faiss_results)}")

    # ------------------------------------------------
    # 2. BM25 keyword search
    # ------------------------------------------------

    print("\nRunning BM25 keyword search...")

    query_tokens = tokenize(question)

    bm25_scores = bm25.get_scores(query_tokens)

    bm25_ranked_indices = sorted(
        range(len(bm25_scores)),
        key=lambda index: bm25_scores[index],
        reverse=True
    )

    bm25_results = [
        bm25_documents[index]
        for index in bm25_ranked_indices[:candidate_k]
        if bm25_scores[index] > 0
    ]

    print(f"BM25 results: {len(bm25_results)}")

    # ------------------------------------------------
    # 3. Reciprocal Rank Fusion
    # ------------------------------------------------

    print("\nCombining results using RRF...")

    fused_results = reciprocal_rank_fusion(
        faiss_results,
        bm25_results,
        rrf_k=RRF_K
    )

    final_results = fused_results[:final_k]

    # ------------------------------------------------
    # 4. Display final ranked results
    # ------------------------------------------------

    print("\n" + "=" * 65)
    print("FARMING CHITTI - HYBRID SEARCH RESULTS")
    print("=" * 65)

    for rank, result in enumerate(final_results, start=1):

        document = result["document"]

        print(f"\nResult {rank}")
        print("-" * 50)

        print(
            f"RRF score: {result['rrf_score']:.6f}"
        )

        print(
            f"Source: {document.metadata.get('source')}"
        )

        print(
            f"Page: {document.metadata.get('page')}"
        )

        print(
            f"Chunk ID: {document.metadata.get('chunk_id')}"
        )

        print("\nContent:")
        print(document.page_content[:1000])

    return final_results


if __name__ == "__main__":

    question = input(
        "\nAsk Farming Chitti a question: "
    )

    hybrid_search(
        question,
        candidate_k=10,
        final_k=5
    )
