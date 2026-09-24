"""
readiness_tool.py — calculate_readiness_score()

The score is ALWAYS computed by this deterministic formula, never by the LLM.
The LLM's only job (in agents/knowledge_agent.py) is to explain the score in
words afterwards. This is important to say explicitly in the viva: the number
is math, not a language-model guess.

Formula (weights sum to 100):
    Skills Match      : 40%  — matched required skills / total required skills
    Resume Quality     : 20%  — presence of key resume sections/signals
    Mock Test Score    : 20%  — latest mock test percentage, if taken
    Mock Interview     : 20%  — latest interview evaluation score, if taken

If mock test / interview haven't been attempted yet, their weight is
redistributed proportionally across whatever HAS been measured, so a student
who hasn't done a mock interview yet still gets a meaningful score instead of
an artificially low one.
"""
from typing import Dict, List, Optional


def _skills_match_pct(detected_skills: List[str], required_skills: List[str]) -> float:
    if not required_skills:
        return 0.0
    detected_lower = {s.strip().lower() for s in detected_skills}
    required_lower = {s.strip().lower() for s in required_skills}
    matched = detected_lower & required_lower
    return round(len(matched) / len(required_lower) * 100, 1)


def _resume_quality_pct(resume_signals: Dict) -> float:
    """resume_signals: dict of booleans like has_projects, has_education,
    has_contact_info, has_measurable_results, word_count_ok."""
    checks = [
        resume_signals.get("has_projects", False),
        resume_signals.get("has_education", False),
        resume_signals.get("has_contact_info", False),
        resume_signals.get("has_measurable_results", False),
        resume_signals.get("word_count_ok", False),
    ]
    return round(sum(1 for c in checks if c) / len(checks) * 100, 1)


def calculate_readiness_score(
    detected_skills: List[str],
    required_skills: List[str],
    resume_signals: Optional[Dict] = None,
    mock_test_pct: Optional[float] = None,
    mock_interview_pct: Optional[float] = None,
) -> Dict:
    resume_signals = resume_signals or {}

    components = {
        "skills_match": {"weight": 40, "value": _skills_match_pct(detected_skills, required_skills)},
        "resume_quality": {"weight": 20, "value": _resume_quality_pct(resume_signals)},
    }
    if mock_test_pct is not None:
        components["mock_test"] = {"weight": 20, "value": round(mock_test_pct, 1)}
    if mock_interview_pct is not None:
        components["mock_interview"] = {"weight": 20, "value": round(mock_interview_pct, 1)}

    total_weight = sum(c["weight"] for c in components.values())
    # Redistribute weight proportionally if some components are missing.
    final_score = 0.0
    for c in components.values():
        normalized_weight = c["weight"] / total_weight * 100
        final_score += c["value"] * (normalized_weight / 100)
        c["normalized_weight"] = round(normalized_weight, 1)

    matched_skills = sorted(set(s.lower() for s in detected_skills) & set(s.lower() for s in required_skills))
    missing_skills = sorted(set(s.lower() for s in required_skills) - set(s.lower() for s in detected_skills))

    return {
        "score": round(final_score, 1),
        "components": components,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }
