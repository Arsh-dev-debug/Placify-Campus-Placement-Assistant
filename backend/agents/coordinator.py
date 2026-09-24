import re
from typing import Dict

from agents.knowledge_agent import answer_question


GREETING_PATTERNS = [
    r"^\s*hi\b",
    r"^\s*hello\b",
    r"^\s*hey\b",
    r"^\s*what can you do\b"
]


def classify_intent(message: str) -> str:

    text = message.lower().strip()

    if any(re.search(pattern, text) for pattern in GREETING_PATTERNS):
        return "greeting"

    return "question"


def handle_message(message: str) -> Dict:

    intent = classify_intent(message)

    if intent == "greeting":
        return {
            "answer": (
                "Hi! I'm your Campus Placement Assistant. "
                "You can ask me about companies, eligibility, "
                "skills, DSA, Java, SQL, interviews, resumes, "
                "mock tests, or placement preparation."
            ),
            "sources": [],
            "mode": "greeting"
        }

    return answer_question(message)