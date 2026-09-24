"""
resume_tool.py — analyze_resume()

Deterministic skill extraction via keyword matching against a known skills
list (SKILL_VOCABULARY). Simple on purpose — this is a beginner-friendly
project and a transparent keyword match is easier to explain in a viva than
an opaque model call, and it's good enough for a resume analyzer demo.

Extend SKILL_VOCABULARY as needed; it's the single source of truth for what
counts as a "detected skill".
"""
import re
from typing import Dict, List

SKILL_VOCABULARY = [
    "python", "java", "c++", "c", "javascript", "typescript", "sql", "html",
    "css", "react", "node.js", "django", "flask", "fastapi", "git", "github",
    "docker", "kubernetes", "aws", "azure", "gcp", "data structures",
    "algorithms", "oop", "dbms", "operating systems", "computer networks",
    "system design", "machine learning", "deep learning", "pandas", "numpy",
    "tensorflow", "pytorch", "power bi", "tableau", "excel", "statistics",
    "rest api", "microservices", "linux", "agile", "scrum",
]


def extract_skills(resume_text: str) -> List[str]:
    text_lower = resume_text.lower()
    found = []
    for skill in SKILL_VOCABULARY:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found


def extract_resume_signals(resume_text: str) -> Dict[str, bool]:
    text_lower = resume_text.lower()
    word_count = len(resume_text.split())
    return {
        "has_projects": bool(re.search(r"\bprojects?\b", text_lower)),
        "has_education": bool(re.search(r"\b(education|b\.?e\.?|b\.?tech|university|college)\b", text_lower)),
        "has_contact_info": bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text)),
        "has_measurable_results": bool(re.search(r"\d+%|\d+\+|\bincreased\b|\breduced\b|\bimproved\b", text_lower)),
        "word_count_ok": 150 <= word_count <= 1200,
    }


def analyze_resume(resume_text: str, required_skills: List[str]) -> Dict:
    detected = extract_skills(resume_text)
    signals = extract_resume_signals(resume_text)
    detected_set = set(detected)
    required_set = {s.lower() for s in required_skills}

    return {
        "detected_skills": sorted(detected_set),
        "suggested_skills": sorted(required_set - detected_set),
        "resume_signals": signals,
    }


def generate_resume_feedback(resume_signals: Dict[str, bool], suggested_skills: List[str]) -> Dict:
    """Deterministic strengths / weaknesses / suggestions for the ATS-style
    report — no LLM guesswork, just rules over the signals we already
    extracted. Clearly labeled as rule-based, not an official ATS score."""
    strengths, weaknesses, suggestions = [], [], []

    if resume_signals.get("has_projects"):
        strengths.append("Includes a projects section — good, recruiters look for applied work.")
    else:
        weaknesses.append("No clear projects section found.")
        suggestions.append("Add a Projects section with 2–3 relevant projects and what you built.")

    if resume_signals.get("has_measurable_results"):
        strengths.append("Uses measurable results (numbers/percentages) — strengthens impact.")
    else:
        weaknesses.append("Descriptions lack measurable outcomes.")
        suggestions.append("Quantify achievements where possible (e.g. 'reduced load time by 30%').")

    if resume_signals.get("has_contact_info"):
        strengths.append("Contact information is present and detectable.")
    else:
        weaknesses.append("Couldn't detect a clear email/contact line.")
        suggestions.append("Make sure your email is clearly visible near the top of the resume.")

    if resume_signals.get("has_education"):
        strengths.append("Education section is present.")
    else:
        weaknesses.append("No clear education section found.")
        suggestions.append("Add an Education section with degree, institution, and CGPA.")

    if not resume_signals.get("word_count_ok"):
        weaknesses.append("Resume length looks off (too short or too long for a clean ATS scan).")
        suggestions.append("Aim for roughly 1 page (300–700 words) for an entry-level resume.")

    if suggested_skills:
        suggestions.append(
            f"Consider adding/learning these role-relevant skills: {', '.join(suggested_skills)}."
        )

    return {"strengths": strengths, "weaknesses": weaknesses, "suggestions": suggestions}
