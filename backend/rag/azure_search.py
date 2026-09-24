"""
azure_search.py — Azure AI Search retrieval.

Not called until retrieval.py detects AZURE_SEARCH_ENDPOINT and
AZURE_SEARCH_KEY are set in .env. Until then, the app runs entirely on
local TF-IDF search (see retrieval.py).

WHEN YOU'RE READY TO CONNECT AZURE:
1. Create an Azure AI Search resource + index (fields: id, content, source,
   section, subsection).
2. Ingest knowledge_base/*.md into that index (chunked the same way
   loader.py does it — one document per subsection).
3. Fill in .env:
     AZURE_SEARCH_ENDPOINT=https://<your-search-name>.search.windows.net
     AZURE_SEARCH_KEY=<admin-or-query-key>
     AZURE_SEARCH_INDEX=<your-index-name>
4. Restart the backend — retrieval.py automatically switches to this file.
"""
import os
from typing import List, Dict

import requests

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX", "placement-knowledge")
AZURE_SEARCH_API_VERSION = "2023-11-01"


def search_azure(query: str, top_k: int = 3) -> List[Dict]:
    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_SEARCH_INDEX}/docs/search?api-version={AZURE_SEARCH_API_VERSION}"
    headers = {"Content-Type": "application/json", "api-key": AZURE_SEARCH_KEY}
    body = {"search": query, "top": top_k}

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[PlacementAgent] Azure AI Search call failed: {e}")
        return []

    results = []
    for doc in data.get("value", []):
        results.append({
            "content": doc.get("content", ""),
            "source": doc.get("source", ""),
            "section": doc.get("section", ""),
            "subsection": doc.get("subsection", ""),
            "score": doc.get("@search.score", 0.0),
        })
    return results
