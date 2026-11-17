
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_chat_model():
    """Initialize the OpenAI chat model."""

    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Check your .env file."
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


def rewrite_followup_question(
    current_question,
    conversation_history=None
):
    """
    Rewrite a follow-up question as a standalone search query.

    conversation_history:
        List of previous farmer questions, in chronological order.

    Returns:
        A standalone question suitable for document retrieval.
    """

    if not current_question or not current_question.strip():
        raise ValueError("Please enter a valid question.")

    conversation_history = conversation_history or []

    # No history means no rewriting is required.
    if not conversation_history:
        return current_question.strip()

    history_text = "\n".join(
        [
            f"Farmer question {index + 1}: {question}"
            for index, question in enumerate(
                conversation_history[-6:]
            )
        ]
    )

    system_prompt = """
You are a query rewriting assistant for Farming Chitti,
an agricultural government schemes knowledge assistant.

Your task is to rewrite a farmer's latest question into
a standalone search query using the conversation history.

Rules:
1. Resolve references such as it, they, this scheme,
   that benefit, and how much using the conversation history.
2. Preserve scheme names, crop names, locations,
   dates, amounts, and other important entities.
3. Do not answer the farmer's question.
4. Do not invent facts or add assumptions.
5. Preserve the original language of the latest question.
6. If the latest question is already standalone,
   keep its meaning and wording as close as possible.
7. Return only the rewritten question.
8. If the reference cannot be resolved confidently,
   return the original question unchanged.
"""

    user_prompt = f"""
Previous farmer questions:
{history_text}

Latest farmer question:
{current_question}

Return the standalone search query only.
"""

    model = get_chat_model()

    response = model.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
    )

    rewritten_question = response.content

    if not isinstance(rewritten_question, str):
        raise ValueError(
            "The query rewriting model returned an unexpected response."
        )

    rewritten_question = rewritten_question.strip().strip('"')

    if not rewritten_question:
        return current_question.strip()

    return rewritten_question


if __name__ == "__main__":

    history = [
        "What is the PM-KISAN scheme?",
        "Who is eligible for this scheme?"
    ]

    question = "How much money will they receive?"

    rewritten = rewrite_followup_question(
        question,
        history
    )

    print("\nOriginal question:")
    print(question)

    print("\nRewritten question:")
    print(rewritten)
