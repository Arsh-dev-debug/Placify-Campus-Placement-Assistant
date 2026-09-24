"""
resume_agent.py — orchestrates resume parsing -> skill extraction ->
role requirement retrieval (RAG) -> ATS score + enhancement suggestions.
"""
from typing import Dict, Optional

from resume.parser import extract_text
from tools.resume_tool import analyze_resume, generate_resume_feedback
from tools.readiness_tool import calculate_readiness_score
from rag.retrieval import search_knowledge_base
from rag.loader import load_chunks


def _get_role_required_skills(target_role: str) -> tuple:
    """
    Exact section-match lookup instead of fuzzy semantic search. This matters
    because "required skills for Software Developer" can semantically match
    OTHER roles' "Required Skills" sections too (they share a lot of generic
    vocabulary), which would silently pollute the skill-gap comparison.
    Falls back to fuzzy RAG search only if no exact role match exists in the
    knowledge base (e.g. the student picked a role we don't have data for).
    """
    chunks = load_chunks()
    exact = [
        c for c in chunks
        if c["section"].strip().lower() == target_role.strip().lower()
        and c["subsection"].strip().lower() == "required skills"
    ]
    if exact:
        skills = [s.strip() for s in exact[0]["text"].split(",") if s.strip()]
        source = [f"{exact[0]['source']} → {exact[0]['section']} → {exact[0]['subsection']}"]
        return skills, source

    # Fallback: fuzzy search, still filtered to only "Required Skills" subsections.
    fuzzy = search_knowledge_base(f"required skills for {target_role}", top_k=3)
    skills, source = [], []
    for r in fuzzy:
        if r["subsection"].lower() == "required skills":
            skills.extend([s.strip() for s in r["content"].split(",") if s.strip()])
            source.append(f"{r['source']} → {r['section']} → {r['subsection']}")
            break  # only take the single best matching role, not all of them
    return skills, source


def process_resume(
    file_bytes: bytes,
    filename: str,
    target_role: str,
    mock_test_pct: Optional[float] = None,
    mock_interview_pct: Optional[float] = None,
) -> Dict:
    resume_text = extract_text(file_bytes, filename)

    required_skills, required_skills_source = _get_role_required_skills(target_role)

    analysis = analyze_resume(resume_text, required_skills)

    ats_score = calculate_readiness_score(
        detected_skills=analysis["detected_skills"],
        required_skills=[s.lower() for s in required_skills],
        resume_signals=analysis["resume_signals"],
        mock_test_pct=mock_test_pct,
        mock_interview_pct=mock_interview_pct,
    )

    feedback = generate_resume_feedback(analysis["resume_signals"], analysis["suggested_skills"])

    return {
        "target_role": target_role,
        "detected_skills": analysis["detected_skills"],
        "suggested_skills": analysis["suggested_skills"],
        "resume_signals": analysis["resume_signals"],
        "required_skills_source": required_skills_source,
        "ats_score": ats_score,
        "strengths": feedback["strengths"],
        "weaknesses": feedback["weaknesses"],
        "suggestions": feedback["suggestions"],
    }
