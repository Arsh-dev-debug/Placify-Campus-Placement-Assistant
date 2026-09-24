# Campus Placement Assistant Agent (Placify)

A student-facing campus-placement preparation platform built as an **Agent + RAG + deterministic Tools** system.

Placify brings resume analysis, role-skill matching, mock tests, mock interviews, and a placement knowledge chatbot into one dashboard. The prototype is designed to run **locally with zero Azure cost**; Microsoft Foundry and Azure AI Search are optional integrations for the LLM and cloud retrieval layers.

## What the project solves

Placement preparation is usually scattered across resume checkers, practice-test websites, interview videos, and company-specific information. Placify combines those workflows and keeps company/role facts grounded in a small, explicit knowledge base.

The system is intentionally split into:

- **Deterministic logic** for resume parsing, skill matching, readiness scoring, question banks, and test scoring.
- **RAG retrieval** for company/role knowledge.
- **LLM feedback** through Microsoft Foundry when Azure is configured.
- **Fallback behavior** that stays explicit instead of inventing company-specific facts.

## Features

### 1. Resume Analysis

Upload a PDF, DOCX, or TXT resume and choose a target role.

The backend:

1. extracts resume text;
2. detects skills using a transparent vocabulary;
3. loads the target role's required skills from the knowledge base;
4. compares detected vs required skills;
5. checks structural resume signals such as projects, education, contact information, measurable results, and word count;
6. returns a deterministic analysis and readiness data.

The skill lookup uses an **exact role/category match first**, avoiding the previous problem where fuzzy retrieval could accidentally pull another role's requirements.

> The displayed score is a prototype readiness/ATS-style estimate, not an employer's ATS decision.

### 2. Mock Tests

Role + difficulty based question banks are stored in code and can be generated through the backend. The frontend now calls both:

- `POST /mock-test/generate`
- `POST /mock-test/score`

The final mock-test percentage is fed into the readiness calculation instead of using a hardcoded dashboard number.

### 3. Mock Interviews

The frontend is wired to the backend interview endpoints:

- `POST /interview/questions`
- `POST /interview/evaluate`

Supported technical question banks currently include **Microsoft, Amazon, and TCS**, plus a generic HR round. Interview evaluation uses Microsoft Foundry when configured and a clearly labelled structural fallback otherwise.

The resulting interview percentage is included in the readiness calculation.

### 4. Placement Knowledge Chat

The chat assistant answers placement-related questions using the placement knowledge base through RAG.

The local RAG implementation uses **TF-IDF**. The same retrieval interface can switch to **Azure AI Search** when the Azure environment variables are configured.

If the placement knowledge base does not contain a company-specific fact, the agent is instructed not to invent one.

## Architecture

### Overview

![Campus Placement Assistant architecture](docs/architecture-overview.png)

### Detailed architecture

![Detailed Campus Placement Assistant architecture](docs/architecture-detailed.png)

### Runtime flow

```text
Student
  |
  v
Placify Frontend (HTML / Tailwind / JS)
  |
  | REST
  v
FastAPI Backend
  |
  +---------------------> /chat
  |                         |
  |                         v
  |                   Coordinator Agent
  |                         |
  |                         v
  |                   Knowledge Agent
  |                         |
  |                         v
  |                  RAG Retrieval Layer
  |                    /             \\
  |             Local TF-IDF       Azure AI Search
  |                    |               |
  |                    +-------+-------+
  |                            v
  |                       Knowledge Base
  |
  +---------------------> /resume/analyze
  |                         |
  |                         v
  |                    Resume Agent
  |                    /           \\
  |             Resume Parser    ATS/Readiness Tool
  |
  +---------------------> /mock-test/*
  |                         |
  |                         v
  |                    Test Tool
  |
  +---------------------> /interview/*
                            |
                            v
                       Interview Tool
                            |
                            v
                 Microsoft Foundry (optional)
```

The high-level diagram intentionally separates deterministic tools from the RAG/LLM layer. The current FastAPI implementation exposes resume, mock-test, and interview workflows as dedicated API routes, while `/chat` goes through the Coordinator/Knowledge Agent path.

## Readiness scoring formula

The backend uses `backend/tools/readiness_tool.py` as the single source of truth for the readiness calculation.

| Component | Weight | Measurement |
|---|---:|---|
| Skills Match | 40% | matched required skills / total required skills |
| Resume Quality | 20% | five structural resume signals |
| Mock Test | 20% | latest mock-test percentage |
| Mock Interview | 20% | latest interview evaluation percentage |

If a mock test or interview has not been attempted, the backend redistributes the available weight across the components that have been measured. The frontend now displays the actual backend component structure rather than the previous hardcoded 40/35/25 three-pillar layout.

## RAG knowledge base

The current knowledge base is **JSON**, not Markdown:

```text
knowledge_base/
├── companies.json
├── roles.json
└── roles_and_skills.json
```

`backend/rag/loader.py` normalizes these records into a common chunk format:

```text
{
  "id": "companies.json::Microsoft::Eligibility",
  "source": "companies.json",
  "section": "Microsoft",
  "subsection": "Eligibility",
  "text": "..."
}
```

The loader also supports older `.md` knowledge files for backward compatibility and de-duplicates identical role records.

## Tech stack

- **Frontend:** HTML, Tailwind CSS, vanilla JavaScript
- **Backend:** Python, FastAPI
- **Resume parsing:** PyPDF2, python-docx, TXT parsing
- **Local retrieval:** scikit-learn TF-IDF + cosine similarity
- **Knowledge store:** JSON files in `knowledge_base/`
- **Cloud retrieval (optional):** Azure AI Search
- **LLM (optional):** Microsoft Foundry / Azure AI Projects

## Project structure

```text
campus-placement-assistant/
├── backend/
│   ├── agents/
│   │   ├── coordinator.py
│   │   ├── knowledge_agent.py
│   │   ├── llm_client.py
│   │   └── resume_agent.py
│   ├── rag/
│   │   ├── azure_search.py
│   │   ├── loader.py
│   │   └── retrieval.py
│   ├── resume/
│   │   └── parser.py
│   ├── tools/
│   │   ├── interview_tool.py
│   │   ├── readiness_tool.py
│   │   ├── resume_tool.py
│   │   └── test_tool.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html
├── knowledge_base/
│   ├── companies.json
│   ├── roles.json
│   └── roles_and_skills.json
├── docs/
│   ├── architecture-overview.png
│   └── architecture-detailed.png
├── .gitignore
└── README.md
```

## Run locally

### 1. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start FastAPI

From the `backend` directory:

```bash
uvicorn main:app --reload --port 8000
```

### 4. Open the frontend

Open:

```text
frontend/index.html
```

The dashboard expects the backend at:

```text
http://localhost:8000
```

The frontend performs a `/health` check and shows whether the backend is reachable.

## Azure / Microsoft Foundry setup (optional)

The project is deliberately usable without Azure.

1. Copy `backend/.env.example` to `backend/.env`.
2. Add your own Microsoft Foundry project endpoint and agent name.
3. If Azure AI Search is required, add the Search endpoint, key, and index name.
4. Restart FastAPI.

The Foundry client is now **lazy-loaded**. Importing the backend does not require Azure CLI, a Windows-specific CLI path, or valid Azure credentials. If Azure is unavailable, the application stays in local/fallback mode.

### Azure AI Search index shape

The optional Search index should expose these fields:

```text
id
content
source
section
subsection
```

The local loader produces the same logical fields, so the retrieval layer can switch implementations without changing the Knowledge Agent API.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Backend/Azure configuration health check |
| POST | `/chat` | Placement knowledge chat |
| POST | `/resume/analyze` | Resume parsing, role skill matching, readiness calculation |
| POST | `/readiness` | Recalculate readiness from the current four components |
| POST | `/mock-test/generate` | Generate role/difficulty question bank |
| POST | `/mock-test/score` | Score submitted mock-test answers |
| POST | `/interview/questions` | Generate HR/company-specific interview questions |
| POST | `/interview/evaluate` | Evaluate an interview answer |

The old unauthenticated `/debug-rag` route has been removed.

## Security and privacy

- **No Azure secrets are included in this project package.** `backend/.env` is intentionally excluded; use `.env.example` as the template.
- `.gitignore` excludes `.env`, Python caches, IDE files, and temporary runner files.
- Uploaded resumes are read into memory for the request and are not intentionally persisted by the prototype.
- The prototype does not implement authentication or authorization, so it should not be exposed directly to the public internet without additional security controls.
- CORS is currently permissive for local development and should be restricted to the deployed frontend origin before production deployment.
- If any Azure credential was ever committed to, uploaded with, or shared from an earlier version of this project, **rotate/revoke that credential in Azure before using the resource again**.

## Known limitations

- The knowledge base is intentionally small and hand-written for the prototype.
- Company eligibility and interview information is sample placement knowledge, not an official employer hiring policy unless independently verified for the relevant campus drive.
- Local TF-IDF is lexical retrieval; it is not semantic/vector search.
- Interview fallback scoring checks answer structure/length only. Richer semantic feedback requires Microsoft Foundry.
- The prototype has no user authentication, database, persistent profile, or production-grade rate limiting.
- The current frontend still contains some offline/demo UI fallbacks, but company-specific chat responses are no longer fabricated when the backend is offline.

## Testing checklist

Before a demo, verify:

1. `GET /health` returns `status: ok`.
2. `POST /chat` retrieves a known company fact from the JSON knowledge base.
3. A resume analysis returns detected skills and role-specific missing skills.
4. `/mock-test/generate` returns questions and `/mock-test/score` updates readiness.
5. `/interview/questions` returns the selected company's technical bank or the HR bank.
6. `/interview/evaluate` returns feedback and a score.
7. `/readiness` shows the four-component 40/20/20/20 formula.
8. No `.env`, `__pycache__`, `.pyc`, or temporary runner files are present in the submitted archive.

## Responsible AI

- Readiness and ATS-style numbers are deterministic prototype estimates, not hiring decisions.
- Company-specific claims should come from the knowledge base rather than an unsupported model guess.
- When the RAG layer has no relevant placement context, the Knowledge Agent is instructed to state that limitation instead of inventing a company-specific fact.
- Interview feedback is practice feedback and should not be presented as an employer's assessment.

## Team

- **Arsh** — Data / Knowledge Lead
- **Deeya** — Backend / Tools Lead
- **Ria** — Agent Lead
- **Bhavana** — Frontend / Demo Lead