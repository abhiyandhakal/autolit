import requests

ARXIV_BASE_URL = "http://export.arxiv.org/api/query"

async def fetch_arxiv_results(keyword: str):
    """Fetch results from the arXiv API."""
    params = {
        "search_query": f"all:{keyword}",
        "start": 0,
        "max_results": 5,
    }
    
    try:
        response = requests.get(ARXIV_BASE_URL, params=params)
        if response.status_code != 200:
            print(f"arXiv API Error: HTTP {response.status_code}")
            print(f"Response Text: {response.text}")  # Log the response for debugging
            return []
        
        # Debugging: Ensure the response body is non-empty and valid
        if not response.text.strip():
            print("arXiv API returned an empty response.")
            return []
        
        # Parse the response
        # For now, assuming the response is in JSON format. Replace with XML parsing if needed.
        response_data = response.json()  # Potential source of the error
        papers = []
        for entry in response_data.get("entries", []):  # Example structure
            papers.append({
                "title": entry.get("title"),
                "authors": entry.get("authors"),
                "link": entry.get("id"),
            })
        return papers
    
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"Response Text: {response.text}")  # Log for further analysis
        return []
    except Exception as e:
        print(f"Unexpected error in arXiv API: {e}")
        return []
