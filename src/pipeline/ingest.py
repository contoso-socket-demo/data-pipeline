"""Settlement file ingestion.

WIRED: requests 2.25.0 is a direct dependency and pulls urllib3 1.26.x
transitively, which is where several of this repo's transitive CVEs live.
"""
import requests


def fetch_batch(url: str, timeout: int = 30) -> bytes:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.content


def post_receipt(url: str, payload: dict) -> int:
    return requests.post(url, json=payload, timeout=30).status_code
