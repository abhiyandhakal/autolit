from app.apis.arxiv import fetch_arxiv_data
import json

def retrieve_papers():
    query = "Artificial Intelligence and Law"
    papers = fetch_arxiv_data(query, start=0, max_results=10)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=4)
    
    print(f"Retrieved {len(papers)} papers related to '{query}' and saved to output.json")


if __name__ == "__main__":
    retrieve_papers()