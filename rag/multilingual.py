
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_model():
    load_dotenv(PROJECT_ROOT / ".env")

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )


def translate_query_for_retrieval(question, source_language):
    """
    Convert a regional-language question into an English
    search query. Preserve scheme names and key entities.
    """
    if source_language.lower() == "english":
        return question

    prompt = f"""
You are a multilingual search-query translator for an
Indian agricultural government schemes assistant.

Translate the farmer's question into a concise English
search query for retrieving government scheme documents.

Rules:
- Preserve scheme names such as PM-KISAN, PMFBY and KCC.
- Preserve names of government departments and places.
- Preserve the exact meaning of the question.
- Do not answer the question.
- Do not add facts or assumptions.
- Return only the English search query.

Original language: {source_language}
Farmer's question: {question}
"""

    response = get_model().invoke(prompt)

    translated_query = response.content

    if not isinstance(translated_query, str):
        translated_query = str(translated_query)

    return translated_query.strip()


def get_language_instruction(language):
    return (
        f"Respond entirely in {language}. "
        "Use simple, farmer-friendly wording. "
        "Keep official scheme names and document references "
        "unchanged where appropriate."
    )
