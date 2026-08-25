"""Minimal arXiv preprints API call — one typed row per paper.

Docs & schema: https://quanticdata.io/collectors/arxiv-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/arxiv_papers/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "query": "mixture of experts",
        "sort": "latest",
        "max_results": 10
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("arxiv_id"), row.get("title"), row.get("abstract"))
print(f"{len(data['results'])} papers, cost ${data['cost']}")
