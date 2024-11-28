import requests

UNPAYWALL_API_BASE_URL = "https://api.unpaywall.org/v2/"
UNPAYWALL_EMAIL = "your_email_here"  # Replace with your registered email

async def fetch_unpaywall_results(keyword: str):
    """Fetch results from the Unpaywall API using DOIs (example implementation)."""
    # Unpaywall typically uses DOIs as input. You might need to pre-fetch DOIs first.
    # This is a placeholder for demonstration purposes.
    doi = "10.1038/s41586-020-2649-2"  # Replace with actual DOIs fetched by another service

    response = requests.get(f"{UNPAYWALL_API_BASE_URL}{doi}", params={"email": UNPAYWALL_EMAIL})
    if response.status_code != 200:
        return []
    
    data = response.json()
    papers = [{
        "title": data.get("title"),
        "authors": [author.get("name") for author in data.get("z_authors", [])],
        "link": data.get("best_oa_location", {}).get("url"),
    }]
    return papers
