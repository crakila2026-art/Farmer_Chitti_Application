
import json
import csv
from pathlib import Path

from rag.query_rewriter import rewrite_followup_question
from rag.answer_generator import generate_answer, build_evidence_context
from retrieval.hybrid_search import hybrid_search
from rag.evidence_validator import validate_answer
from rag.language_support import get_language_from_choice, detect_language_from_text
from rag.multilingual import translate_query_for_retrieval

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "evaluation_dataset.json"
RESULT_PATH = BASE_DIR.parent / "test_results" / "evaluation_results.csv"


def calculate_keyword_coverage(answer, keywords):

    if not keywords:
        return 0.0

    answer = answer.lower()

    matched = sum(
        1 for keyword in keywords
        if keyword.lower() in answer
    )

    return matched / len(keywords)


def run_evaluation():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)

    results = []

    for test in dataset:

        question = test["question"]

        print(f"\nEvaluating Test {test['id']}: {question}")

        try:

            response_language = detect_language_from_text(question)

            rewritten_question = rewrite_followup_question(
                current_question=question,
                conversation_history=[]
            )

            retrieval_query = translate_query_for_retrieval(
                rewritten_question,
                response_language
            )

            retrieved_results = hybrid_search(
                retrieval_query,
                candidate_k=10,
                final_k=5
            )

            result = generate_answer(
                question=question,
                retrieved_results=retrieved_results,
                response_language=response_language
            )

            evidence_context, sources = build_evidence_context(
                retrieved_results
            )

            validation = validate_answer(
                answer=result["answer"],
                evidence_context=evidence_context
            )

            coverage = calculate_keyword_coverage(
                result["answer"],
                test["expected_keywords"]
            )

            source_match = any(
                test["expected_source"].lower() in str(source).lower()
                for source in sources
            )

            results.append({
                "test_id": test["id"],
                "question": question,
                "language": test["language"],
                "keyword_coverage": round(coverage, 2),
                "evidence_valid": validation["is_valid"],
                "source_match": source_match,
                "status": (
                    "PASS"
                    if validation["is_valid"] and source_match
                    else "REVIEW"
                ),
                "answer": result["answer"],
                "sources": str(sources)
            })

        except Exception as error:

            results.append({
                "test_id": test["id"],
                "question": question,
                "language": test["language"],
                "keyword_coverage": 0,
                "evidence_valid": False,
                "source_match": False,
                "status": "ERROR",
                "answer": str(error),
                "sources": ""
            })

    with open(RESULT_PATH, "w", newline="", encoding="utf-8-sig") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    total = len(results)
    passed = sum(r["status"] == "PASS" for r in results)

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)
    print("Total tests:", total)
    print("Passed:", passed)
    print("Needs review:", sum(r["status"] == "REVIEW" for r in results))
    print("Errors:", sum(r["status"] == "ERROR" for r in results))
    print("Pass rate:", round(passed / total * 100, 2), "%")
    print("Results saved:", RESULT_PATH)


if __name__ == "__main__":
    run_evaluation()
