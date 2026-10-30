import os
from urllib.parse import quote
import requests
BACKEND_URL=os.getenv("BACKEND_URL","http://127.0.0.1:3030").rstrip("/")
SENTIMENT_URL=os.getenv("SENTIMENT_ANALYZER_URL","http://127.0.0.1:5050").rstrip("/")
def get_request(endpoint):
    r=requests.get(f"{BACKEND_URL}/{endpoint.lstrip('/')}",timeout=20)
    r.raise_for_status()
    return r.json()
def analyze_review_sentiments(text):
    r=requests.get(f"{SENTIMENT_URL}/analyze/{quote(text,safe='')}",timeout=20)
    r.raise_for_status()
    return r.json()
def post_review(data):
    r=requests.post(f"{BACKEND_URL}/insert_review",json=data,timeout=20)
    r.raise_for_status()
    return r.json()
