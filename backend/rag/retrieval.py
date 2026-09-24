"""
retrieval.py — RAG retrieval over the knowledge base.

Two modes, chosen automatically:

1. LOCAL MODE (default, works right now with zero Azure setup):
   TF-IDF search over the chunks parsed from knowledge_base/*.md.

2. AZURE MODE (kicks in automatically once you fill in .env with real values):
   Uses Azure AI Search via azure_search.py. Same function signature.

Whoever calls `search_knowledge_base()` never needs to know which mode is
active — fill in .env later and nothing else changes.
"""
import os
from typing import List, Dict

from .loader import load_chunks

_USE_AZURE = bool(os.getenv("AZURE_SEARCH_ENDPOINT") and os.getenv("AZURE_SEARCH_KEY"))

_chunks_cache: List[Dict] = []
_vectorizer = None
_matrix = None


def _ensure_local_index():
    global _chunks_cache, _vectorizer, _matrix
    if _vectorizer is not None:
        return
    from sklearn.feature_extraction.text import TfidfVectorizer

    _chunks_cache = load_chunks()
    texts = [f"{c['section']} {c['subsection']} {c['text']}" for c in _chunks_cache]
    if not texts:
        _vectorizer = "empty"
        return
    _vectorizer = TfidfVectorizer(stop_words="english")
    _matrix = _vectorizer.fit_transform(texts)


def _search_local(query: str, top_k: int) -> List[Dict]:
    _ensure_local_index()
    if _vectorizer == "empty" or not _chunks_cache:
        return []

    from sklearn.metrics.pairwise import cosine_similarity

    query_vec = _vectorizer.transform([query])
    sims = cosine_similarity(query_vec, _matrix).flatten()

    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    results = []
    for idx, score in ranked[:top_k]:
        if score <= 0:
            continue
        chunk = _chunks_cache[idx]
        results.append({
            "content": chunk["text"],
            "source": chunk["source"],
            "section": chunk["section"],
            "subsection": chunk["subsection"],
            "score": float(score),
        })
    return results


def search_knowledge_base(query: str, top_k: int = 3) -> List[Dict]:
    """RAG retrieval tool — the Coordinator/Knowledge Agent calls this."""
    if _USE_AZURE:
        from .azure_search import search_azure
        return search_azure(query, top_k)

    return _search_local(query, top_k)
