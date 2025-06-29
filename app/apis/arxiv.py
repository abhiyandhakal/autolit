from typing import List
import requests
import xmltodict
import time

ARXIV_URI = "https://export.arxiv.org/api/query"


ARXIV_URI = "https://export.arxiv.org/api/query"
HEADERS = {
    "User-Agent": "YourAppName/1.0 (Contact: your-email@example.com)"
}

'''
Sample query	Error Explanation
http://export.arxiv.org/api/query?start=not_an_int	start must be an integer
http://export.arxiv.org/api/query?start=-1	start must be >= 0
http://export.arxiv.org/api/query?max_results=not_an_int	max_results must be an integer
http://export.arxiv.org/api/query?max_results=-1	max_results must be >= 0
http://export.arxiv.org/api/query?id_list=1234.1234	malformed id - see arxiv identifier explanation
http://export.arxiv.org/api/query?id_list=cond—mat/0709123	malformed id - see arxiv identifier explanation

'''
def validate_arxiv_query_params(start: int, max_results: int):
    if not isinstance(start, int) or start < 0:
        raise ValueError("start must be a non-negative integer")
    if not isinstance(max_results, int) or max_results <= 0:
        raise ValueError("max_results must be a positive integer")

def fetch_arxiv_data(query: str, start: int = 0, max_results: int = 10, retries: int = 3, delay: float = 3.0) -> List[dict]:
    validate_arxiv_query_params(start, max_results)

    params = {
        'search_query': query,
        'start': start,
        'max_results': max_results
    }

    for attempt in range(retries):
        try:
            response = requests.get(ARXIV_URI, params=params, headers=HEADERS, timeout=10)
            response.raise_for_status()

            if not response.text.strip():
                raise Exception("Empty response from arXiv")

            parsed_response = xmltodict.parse(response.text)
            entries = parsed_response.get('feed', {}).get('entry', [])

            if isinstance(entries, dict):
                entries = [entries]

            if not entries:
                return []

            papers = []
            for entry in entries:
                authors_data = entry.get('author', [])
                if isinstance(authors_data, dict):
                    authors = [authors_data.get('name', '')]
                elif isinstance(authors_data, list):
                    authors = [author.get('name', '') for author in authors_data]
                else:
                    authors = []

                categories_data = entry.get('category', [])
                if isinstance(categories_data, dict):
                    categories = [categories_data.get('@term', '')]
                elif isinstance(categories_data, list):
                    categories = [cat.get('@term', '') for cat in categories_data]
                else:
                    categories = []

                links_data = entry.get('link', [])
                if isinstance(links_data, dict):
                    links_data = [links_data]
                links = {link.get('@rel', ''): link.get('@href', '') for link in links_data}

                paper = {
                    'id': entry.get('id', ''),
                    'title': entry.get('title', '').strip(),
                    'summary': entry.get('summary', '').strip(),
                    'published': entry.get('published', ''),
                    'updated': entry.get('updated', ''),
                    'authors': authors,
                    'categories': categories,
                    'links': links
                }

                papers.append(paper)

            time.sleep(delay)  # rate limit
            return papers

        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise Exception(f"Request to arXiv failed after {retries} attempts: {str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while processing the response: {str(e)}")
