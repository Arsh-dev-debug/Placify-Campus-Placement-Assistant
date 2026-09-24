"""
loader.py — parses the knowledge_base/*.md files into chunks for RAG.

Chunk format expected in the .md files:

    ## Company or Role Name
    ### Subsection Title
    <content...>

Each returned chunk is a dict:
    {
        "id": "companies.md::Microsoft::Eligibility",
        "source": "companies.md",
        "section": "Microsoft",
        "subsection": "Eligibility",
        "text": "the raw subsection text",
    }

No external dependencies, so this works with zero Azure setup. Swap this out
for Azure AI Search ingestion later without changing anything that calls
`load_chunks()`.
"""
import os
import re
from typing import List, Dict

KB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge_base")


def _strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def load_chunks(kb_dir: str = KB_DIR) -> List[Dict]:
    chunks: List[Dict] = []

    if not os.path.isdir(kb_dir):
        return chunks

    for filename in sorted(os.listdir(kb_dir)):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(kb_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            raw = _strip_comments(f.read())

        sections = re.split(r"^##\s+", raw, flags=re.MULTILINE)[1:]
        for section_block in sections:
            lines = section_block.split("\n", 1)
            section_title = lines[0].strip()
            rest = lines[1] if len(lines) > 1 else ""

            subsections = re.split(r"^###\s+", rest, flags=re.MULTILINE)[1:]
            for sub_block in subsections:
                sub_lines = sub_block.split("\n", 1)
                sub_title = sub_lines[0].strip()
                body = sub_lines[1].strip() if len(sub_lines) > 1 else ""

                if not body:
                    continue

                chunks.append({
                    "id": f"{filename}::{section_title}::{sub_title}",
                    "source": filename,
                    "section": section_title,
                    "subsection": sub_title,
                    "text": body,
                })

    return chunks
