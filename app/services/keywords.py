import os
from fastapi import HTTPException
import requests


def keyword_gen(title: str, abstract: str) -> list[str]:
    GEMINI_API_URL = os.environ.get("GEMINI_API_URL") or ""
    res = requests.post(GEMINI_API_URL, json={
        "contents": [{
            "parts": [{
                "text": f"""
                    Extract 5–10 relevant and concise keywords from the following
                    research paper title and abstract. Each keyword should be 1–3
                    words long. Return only the keywords as a plain list, one per
                    line. Don't say anything else.

                    Title: {title}

                    Abstract: {abstract}
                """
                }]
            }]
    })

    if not res.ok:
        print(res.json())
        raise HTTPException(status_code=500)

    res = res.json()

    keywords_str: str = res["candidates"][0]["content"]["parts"][0]["text"]
    keywords = keywords_str.split("\n")
    return [keyword for keyword in keywords if keyword.strip() != ""]
