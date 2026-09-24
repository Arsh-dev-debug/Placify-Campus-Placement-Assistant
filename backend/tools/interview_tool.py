"""
interview_tool.py — mock interview questions and answer evaluation.

Question bank is deterministic and keyed by (company_or_role, round_type),
so the demo is fast and reliable. Answer evaluation uses the LLM when
connected (agents/llm_client.py); falls back to a simple deterministic
keyword-overlap check otherwise so the feature still works with zero Azure
setup.
"""
from typing import Dict, List, Optional

from agents.llm_client import generate_response

HR_QUESTIONS = [
    {"q": "Tell me about yourself.",
     "tip": "Keep it to 60–90 seconds: background, key strengths, why this role."},
    {"q": "Why do you want to work at this company?",
     "tip": "Reference something specific about the company/role, not a generic answer."},
    {"q": "What is your biggest strength and weakness?",
     "tip": "Pick a real weakness and show what you're doing to improve it."},
    {"q": "Tell me about a time you faced a challenge in a project and how you handled it.",
     "tip": "Use a STAR structure: Situation, Task, Action, Result."},
    {"q": "Where do you see yourself in 5 years?",
     "tip": "Show ambition that's realistic and aligned with the role/company."},
]

TECHNICAL_QUESTIONS: Dict[str, List[Dict]] = {
    "Microsoft": [
        {"q": "Explain the difference between an array and a linked list.",
         "answer_hint": "arrays contiguous memory fixed size fast index; linked list dynamic size nodes pointers"},
        {"q": "What is time complexity and why does it matter?",
         "answer_hint": "measures how runtime grows with input size, big O notation"},
        {"q": "How would you design a basic file storage system at a high level?",
         "answer_hint": "chunking storage metadata redundancy scalability"},
    ],
    "Amazon": [
        {"q": "Explain Amazon's Leadership Principles and pick one to discuss.",
         "answer_hint": "customer obsession ownership bias for action deliver results"},
        {"q": "What is the difference between a stack and a queue?",
         "answer_hint": "stack LIFO last in first out queue FIFO first in first out"},
        {"q": "How would you scale a service that suddenly gets 10x traffic?",
         "answer_hint": "load balancing horizontal scaling caching autoscaling"},
    ],
    "TCS": [
        {"q": "What is normalization in databases?",
         "answer_hint": "reduce redundancy organize data into tables relationships"},
        {"q": "Explain OOP and its four pillars.",
         "answer_hint": "encapsulation inheritance polymorphism abstraction"},
        {"q": "What is the difference between HTTP and HTTPS?",
         "answer_hint": "HTTPS encrypted secure SSL TLS HTTP not encrypted"},
    ],
}

DEFAULT_TECHNICAL = TECHNICAL_QUESTIONS["Microsoft"]


def get_interview_questions(company: str, round_type: str, num_questions: int = 3) -> List[Dict]:
    round_type = round_type.lower()
    if round_type == "hr":
        return HR_QUESTIONS[:num_questions]

    bank = TECHNICAL_QUESTIONS.get(company, DEFAULT_TECHNICAL)
    return [{"q": q["q"]} for q in bank[:num_questions]]


EVAL_SYSTEM_PROMPT = (
    "You are a mock interview evaluator for a campus placement assistant. "
    "Given a question and a student's answer, give: a score out of 10, 2-3 "
    "short strengths, 1-2 short areas to improve, and one brief suggested "
    "improvement. Be encouraging but honest. Keep the whole response under "
    "120 words. Do not claim this reflects a real employer's judgment."
)


def evaluate_answer(question: str, answer: str) -> Dict:
    user_prompt = f"QUESTION:\n{question}\n\nSTUDENT ANSWER:\n{answer}"
    feedback = generate_response(EVAL_SYSTEM_PROMPT, user_prompt)
    if feedback is not None:
        return {"feedback": feedback, "mode": "llm"}

    return {"feedback": _fallback_evaluation(answer), "mode": "fallback"}


def _fallback_evaluation(answer: str) -> str:
    """Deterministic fallback when no LLM is connected — a simple,
    honest length/structure check, clearly not a full evaluation."""
    word_count = len(answer.split())
    if word_count < 15:
        return (
            "Your answer looks quite short — try expanding with a specific example "
            "or more detail. (Automatic evaluation only checks structure right now; "
            "connect the AI model for full feedback.)"
        )
    return (
        "Answer recorded — has reasonable length and detail. (Automatic evaluation "
        "only checks structure right now; connect the AI model in .env for full "
        "content feedback.)"
    )
