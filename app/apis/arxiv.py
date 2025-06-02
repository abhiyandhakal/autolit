import requests
import xmltodict

ARXIV_URI = "https://export.arxiv.org/api/query"

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

def fetch_arxiv_data(query: str, start: int = 0, max_results: int = 10):
    validate_arxiv_query_params(start, max_results)
    
    params = {
        'search_query': query,
        'start': start,
        'max_results': max_results
    }
    
    try:
        response = requests.get(ARXIV_URI, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching data from arXiv: {response.status_code} - {response.text}")
        

        if not response.text.strip():
            raise Exception("Empty response from arXiv")
        
        parsed_response = xmltodict.parse(response.text)

        entries = parsed_response.get('feed', {}).get('entry', [])

        if isinstance(entries, dict):
            entries = [entries]

        if not entries:
            raise Exception("No entries found in the response from arXiv")

        papers = []

        for entry in entries:
            authors_data = entry.get('author', [])
            if isinstance(authors_data, dict):
                authors = [authors_data.get('name', '')]
            elif isinstance(authors_data, list):
                authors = [author.get('name', '') for author in authors_data]
            elif isinstance(authors_data, str):
                authors = [authors_data]
            else:
                authors = []
                
            paper = {
                'id': entry.get('id', ''),
                'title': entry.get('title', ''),
                'summary': entry.get('summary', ''),
                'published': entry.get('published', ''),
                'updated': entry.get('updated', ''),
                'authors': authors, 
                'categories': [category.get('@term', '') for category in entry.get('category', [])],
                'links': {link.get('@rel', ''): link.get('@href', '') for link in entry.get('link', [])}
            }

            papers.append(paper)

        return papers


    except requests.exceptions.RequestException as e:
        raise Exception(f"Request to arXiv failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred while processing the response: {str(e)}")