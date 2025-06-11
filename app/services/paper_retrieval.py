from app.apis.arxiv import fetch_arxiv_data
import json

def retrieve_papers(keyword):
    return fetch_arxiv_data(keyword, start=0, max_results=10)
