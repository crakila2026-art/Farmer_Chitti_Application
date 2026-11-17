
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from rag.prompts import SYSTEM_PROMPT, build_user_prompt


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_chat_model():

    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing from .env"
        )

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini"
    )

    return ChatOpenAI(
        model=model_name,
        temperature=0,
        api_key=api_key
    )


def build_evidence_context(retrieved_results):
    """
    Prepare retrieved chunks as labelled evidence.

    Returns:
        evidence_context: Text passed to the LLM.
        sources: Actual source metadata for citations.
    """

    evidence_sections = []
    sources = []

    for index, result in enumerate(
        retrieved_results,
        start=1
    ):

        document = result["document"]

        source_id = f"S{index}"

        source_name = document.metadata.get(
            "source", "Unknown source"
        )

        page_number = document.metadata.get(
            "page", "Unknown page"
        )

        chunk_id = document.metadata.get(
            "chunk_id", "Unknown chunk"
        )

        evidence_sections.append(
            f"""
[{source_id}]
Source PDF: {source_name}
Page: {page_number}
Chunk ID: {chunk_id}

Evidence:
{document.page_content}
"""
        )

        sources.append({
            "reference": source_id,
            "source": source_name,
            "page": page_number,
            "chunk_id": chunk_id
        })

    evidence_context = "\n\n".join(evidence_sections)

    return evidence_context, sources


def generate_answer(
    question,
    retrieved_results,
    response_language="English"
):
    """
    Generate an evidence-grounded response.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not retrieved_results:
        return {
            "answer": (
                "I could not find sufficient information "
                "in the uploaded government documents "
                "to answer this question."
            ),
            "sources": []
        }

    evidence_context, sources = build_evidence_context(
        retrieved_results
    )

    model = get_chat_model()

    user_prompt = build_user_prompt(
        question=question,
        evidence_context=evidence_context,
        response_language=response_language
    )

    response = model.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
    )

    answer = response.content

    if not isinstance(answer, str) or not answer.strip():
        raise ValueError(
            "The language model returned an empty answer."
        )

    return {
        "answer": answer.strip(),
        "sources": sources
    }


if __name__ == "__main__":

    from retrieval.hybrid_search import hybrid_search

    test_question = (
        "What information is available about "
        "PM-KISAN in the uploaded documents?"
    )

    retrieved_results = hybrid_search(
        test_question,
        candidate_k=10,
        final_k=5
    )

    result = generate_answer(
        question=test_question,
        retrieved_results=retrieved_results,
        response_language="English"
    )

    print("\n" + "=" * 60)
    print("FARMING CHITTI - GENERATED ANSWER")
    print("=" * 60)

    print(result["answer"])

    print("\nSource references:")

    for source in result["sources"]:
        print(
            f"[{source['reference']}] "
            f"{source['source']} - "
            f"Page {source['page']}"
        )
