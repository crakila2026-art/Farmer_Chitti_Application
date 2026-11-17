
from rag.language_support import (
    get_language_from_choice,
    detect_language_from_text
)


def test_tamil_detection():
    assert detect_language_from_text(
        "விவசாயிகளுக்கு என்ன உதவி கிடைக்கும்?"
    ) == "Tamil"


def test_hindi_detection():
    assert detect_language_from_text(
        "पीएम किसान योजना क्या है?"
    ) == "Hindi"


def test_telugu_detection():
    assert detect_language_from_text(
        "పీఎం కిసాన్ పథకం ఏమిటి?"
    ) == "Telugu"


def test_kannada_detection():
    assert detect_language_from_text(
        "ಪಿಎಂ ಕಿಸಾನ್ ಯೋಜನೆ ಏನು?"
    ) == "Kannada"


def test_malayalam_detection():
    assert detect_language_from_text(
        "പിഎം കിസാൻ പദ്ധതി എന്താണ്?"
    ) == "Malayalam"


def test_english_detection():
    assert detect_language_from_text(
        "What is PM-KISAN?"
    ) == "English"


def test_language_selection():
    assert get_language_from_choice("2") == "Tamil"
    assert get_language_from_choice("3") == "Hindi"
