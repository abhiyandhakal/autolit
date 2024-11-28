import requests

SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

async def fetch_semantic_scholar_results(keyword: str):
    """Fetch results from the Semantic Scholar API."""
    params = {
        "query": keyword,
        "fields": "title,authors,url",
        "limit": 5,
    }
    headers = {"User-Agent": "ResearchPaperFetcher/1.0"}
    
    response = requests.get(SEMANTIC_SCHOLAR_BASE_URL, params=params, headers=headers)
    if response.status_code != 200:
        return []
    
    papers = []
    data = response.json()
    for paper in data.get("data", []):
        papers.append({
            "title": paper.get("title"),
            "authors": [author.get("name") for author in paper.get("authors", [])],
            "link": paper.get("url"),
        })
    return papers
