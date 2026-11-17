
from evaluation.evaluator import calculate_keyword_coverage


def test_all_keywords_found():

    answer = "PM-KISAN provides income support to farmers."

    keywords = ["income support", "farmers"]

    assert calculate_keyword_coverage(answer, keywords) == 1.0


def test_partial_keywords_found():

    answer = "PM-KISAN supports farmers."

    keywords = ["farmers", "income support"]

    assert calculate_keyword_coverage(answer, keywords) == 0.5


def test_no_keywords():

    assert calculate_keyword_coverage("Test answer", []) == 0.0
