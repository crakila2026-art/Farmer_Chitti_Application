
from rag.evidence_validator import check_citations


def test_valid_citation():
    answer = "PM-KISAN provides assistance [S1]."
    evidence = "[S1] PM-KISAN scheme evidence."

    result = check_citations(answer, evidence)
    
    assert result["has_citations"] is True
    assert result["invalid_citations"] == []


def test_invalid_citation():
    answer = "The benefit is available [S3]."
    evidence = "[S1] Retrieved scheme evidence."

    result = check_citations(answer, evidence)

    assert result["invalid_citations"] == ["S3"]


def test_missing_citation():
    answer = "Farmers can apply for the scheme."
    evidence = "[S1] Retrieved scheme evidence."

    result = check_citations(answer, evidence)

    assert result["has_citations"] is False
