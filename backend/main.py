"""
main.py — FastAPI backend for the Campus Placement Assistant Agent.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from agents.coordinator import handle_message
from agents.resume_agent import process_resume
from agents.llm_client import is_azure_active

from tools.test_tool import generate_mock_test, score_mock_test
from tools.interview_tool import get_interview_questions, evaluate_answer


app = FastAPI(title="Campus Placement Assistant Agent")
@app.get("/debug-rag")
def debug_rag():
    import rag.retrieval as retrieval

    results = retrieval.search_knowledge_base(
        "Microsoft Eligibility",
        top_k=3
    )

    return {
        "azure_mode": retrieval._USE_AZURE,
        "chunks_loaded": len(retrieval._chunks_cache),
        "results": results
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class MockTestRequest(BaseModel):
    company: str = "General"
    role: str
    difficulty: str = "medium"
    num_questions: int = 12


class MockTestScoreRequest(BaseModel):
    answers: list


class InterviewQuestionsRequest(BaseModel):
    company: str
    round_type: str = "hr"
    num_questions: int = 3


class InterviewEvaluateRequest(BaseModel):
    question: str
    answer: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "azure_llm_active": is_azure_active()
    }


@app.post("/chat")
def chat(req: ChatRequest):
    return handle_message(req.message)


@app.post("/resume/analyze")
async def resume_analyze(
    file: UploadFile,
    target_role: str = Form(...),
    mock_test_pct: Optional[float] = Form(None),
    mock_interview_pct: Optional[float] = Form(None),
):
    file_bytes = await file.read()

    try:
        result = process_resume(
            file_bytes=file_bytes,
            filename=file.filename,
            target_role=target_role,
            mock_test_pct=mock_test_pct,
            mock_interview_pct=mock_interview_pct,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result


@app.post("/mock-test/generate")
def mock_test_generate(req: MockTestRequest):
    question_count = max(10, min(20, req.num_questions))
    questions = generate_mock_test(req.role, req.difficulty, num_questions=question_count, company=req.company)

    return {
        "company": req.company,
        "role": req.role,
        "difficulty": req.difficulty,
        "num_questions": question_count,
        "questions": questions
    }


@app.post("/mock-test/score")
def mock_test_score(req: MockTestScoreRequest):
    return {
        "score_pct": score_mock_test(req.answers)
    }


@app.post("/interview/questions")
def interview_questions(req: InterviewQuestionsRequest):
    questions = get_interview_questions(
        req.company,
        req.round_type,
        req.num_questions
    )

    return {
        "company": req.company,
        "round_type": req.round_type,
        "questions": questions
    }


@app.post("/interview/evaluate")
def interview_evaluate(req: InterviewEvaluateRequest):
    return evaluate_answer(req.question, req.answer)