import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.test_tool import generate_mock_test


def test_google_company_question_bank_returns_five_questions():
    questions = generate_mock_test("Software Developer", "easy", num_questions=5, company="Google")

    assert len(questions) == 5
    assert all("q" in q and "a" in q for q in questions)


def test_ai_ml_engineer_has_company_specific_question_bank():
    questions = generate_mock_test("AI/ML Engineer", "hard", num_questions=2, company="Microsoft")

    assert len(questions) == 2
    matches = any(
        "model" in q["q"].lower()
        or "bias" in q["q"].lower()
        or "gradient" in q["q"].lower()
        for q in questions
    )
    assert matches
