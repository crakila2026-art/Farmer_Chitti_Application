
import re

SUPPORTED_LANGUAGES = {
    "1": "English",
    "2": "Tamil",
    "3": "Hindi",
    "4": "Telugu",
    "5": "Kannada",
    "6": "Malayalam"
}

LANGUAGE_NAMES = {
    "english": "English",
    "tamil": "Tamil",
    "hindi": "Hindi",
    "telugu": "Telugu",
    "kannada": "Kannada",
    "malayalam": "Malayalam"
}


def get_language_from_choice(choice):
    """Convert the user's menu selection to a language name."""
    return SUPPORTED_LANGUAGES.get(choice, "English")


def detect_language_from_text(text):
    """
    Basic Unicode-script detection.

    This is a lightweight fallback, not a full language detector.
    Shared or ambiguous scripts may need user confirmation.
    """
    if re.search(r"[\u0B80-\u0BFF]", text):
        return "Tamil"

    if re.search(r"[\u0900-\u097F]", text):
        return "Hindi"

    if re.search(r"[\u0C00-\u0C7F]", text):
        return "Telugu"

    if re.search(r"[\u0C80-\u0CFF]", text):
        return "Kannada"

    if re.search(r"[\u0D00-\u0D7F]", text):
        return "Malayalam"

    return "English"


def get_response_language(choice, question):
    """
    Use the selected language when a valid selection is provided.
    Otherwise, infer language from the question's script.
    """
    if choice in SUPPORTED_LANGUAGES:
        return get_language_from_choice(choice)

    return detect_language_from_text(question)
