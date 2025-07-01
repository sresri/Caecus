# summarize.py
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

from googlesearch import search

def search_web(query):
    print("We actually caalled this.")
    results = []
    for url in search(query, stop=5, lang="en"):
        if "google" not in url:
            results.append(url)
    return results



def scrape_content(url):
    print("Scraping: ", url)
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        text = ' '.join([p.text for p in soup.find_all('p')])
        print(text)
        return text[:500]  # Keep it short for summarizer
    except Exception:
        return ""

import requests
import json

OPENROUTER_API_KEY = "REDACTED"

def summarize_text(text, query):
    print("Summarizing: ", text)
    if not text:
        return "No content could be extracted."
    
    try:
        response = requests.post(
            url="REDACTED",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "",
                "X-Title": "",
            },
            data=json.dumps({
                "model": "google/gemma-3n-e4b-it:free",
                "messages": [
                    {
                        "role": "user",
                        "content": "REDACTED"
                    }
                ]
            })
        )

        if response.status_code != 200:
            print("OpenRouter API error:", response.text)
            return "Summarization failed."

        summary = response.json()["choices"][0]["message"]["content"]
        print("SUMMARY SUMMARY: ", summary)
        return summary.strip()

    except Exception as e:
        print("Exception during summarization:", e)
        return "Summarization failed."

