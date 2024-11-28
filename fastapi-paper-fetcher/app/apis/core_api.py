import requests

CORE_API_BASE_URL = "https://api.core.ac.uk/v3/search/works"
CORE_API_KEY = "your_core_api_key_here"  # Replace with your API key

async def fetch_core_results(keyword: str):
    """Fetch results from the CORE API."""
    headers = {
        "Authorization": f"Bearer {CORE_API_KEY}",
    }
    params = {
        "q": keyword,
        "page": 1,
        "pageSize": 5,
    }
    
    response = requests.get(CORE_API_BASE_URL, headers=headers, params=params)
    if response.status_code != 200:
        return []
    
    papers = []
    data = response.json()
    for item in data.get("results", []):
        papers.append({
            "title": item.get("title"),
            "authors": item.get("authors", []),
            "link": item.get("downloadUrl"),
        })
    return papers
