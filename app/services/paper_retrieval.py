from app.apis.arxiv import fetch_arxiv_data
import json

def retrieve_papers(keyword, max_results=20):
    return fetch_arxiv_data(query=keyword, max_results=max_results, start=0)
