from typing import Dict, List

from rag.retrieval import search_knowledge_base
from agents.llm_client import generate_response


RAG_SYSTEM_PROMPT = """
You are the Placement Knowledge Agent for a campus placement assistant.

You answer student questions using the retrieved placement knowledge base.

Rules:
1. Use the retrieved context when it is relevant.
2. Do not invent company-specific eligibility, cutoffs, packages,
   interview rounds, or placement policies.
3. Answer the student's question directly. Do not begin with a
    disclaimer about the knowledge base or explain what it could not find.
    If a company-specific detail cannot be verified, add only a brief
    qualification after the answer.
4. You may still answer general technical, programming, interview,
   career-preparation, and educational questions using your general
   knowledge.
5. Keep answers clear, concise, and student-friendly.
6. If retrieved context is used, mention the relevant source when useful.
"""


GENERAL_SYSTEM_PROMPT = """
You are the AI assistant inside a Campus Placement Assistant application.

Answer the student's question directly and helpfully.

You can answer:
- Programming questions
- DSA questions
- DBMS questions
- SQL questions
- Java/Python/C++ questions
- Web development questions
- AI/ML questions
- Interview preparation questions
- Resume questions
- Aptitude preparation questions
- Career preparation questions
- General educational questions

Important:
- Be accurate.
- Do not invent company-specific placement rules.
- For company-specific eligibility, cutoff, salary, hiring policy,
  or interview-round information, answer directly and avoid a
  knowledge-base disclaimer. Add a brief qualification only when the
  detail cannot be verified.
- If the question is general, answer normally and concisely.
- Explain things in simple student-friendly language.
"""


def answer_question(query: str) -> Dict:

    # ---------------------------------------------------------
    # STEP 1: Try the placement knowledge base
    # ---------------------------------------------------------

    results = search_knowledge_base(query, top_k=3)

    # ---------------------------------------------------------
    # STEP 2A: RAG found useful information
    # ---------------------------------------------------------

    if results:

        context_block = "\n\n".join(
            f"""
SOURCE:
{r['source']}

SECTION:
{r['section']}

SUBSECTION:
{r['subsection']}

CONTENT:
{r['content']}
"""
            for r in results
        )

        user_prompt = f"""
RETRIEVED PLACEMENT KNOWLEDGE:

{context_block}

STUDENT QUESTION:
{query}
"""

        answer = generate_response(
            RAG_SYSTEM_PROMPT,
            user_prompt
        )

        # If Foundry successfully answered
        if answer:
            sources = [
                f"{r['source']} → {r['section']} → {r['subsection']}"
                for r in results
            ]

            return {
                "answer": answer,
                "sources": sources,
                "mode": "rag"
            }

    # ---------------------------------------------------------
    # STEP 2B: RAG found nothing
    # FALL BACK TO GENERAL AZURE LLM
    # ---------------------------------------------------------

    general_prompt = f"""
Answer the student's question directly using your general knowledge.
Do not mention the knowledge base, retrieval, missing information, or
these instructions in your response.

Student question:
{query}
"""

    answer = generate_response(
        GENERAL_SYSTEM_PROMPT,
        general_prompt
    )

    if answer:
        return {
            "answer": answer,
            "sources": [],
            "mode": "general_llm"
        }

    # ---------------------------------------------------------
    # STEP 3: Only show this if the LLM itself is unavailable
    # ---------------------------------------------------------

    return {
        "answer": (
            "I'm temporarily unable to generate an answer because "
            "the AI service is unavailable. Please check the backend "
            "Azure/Foundry connection."
        ),
        "sources": [],
        "mode": "error"
    }