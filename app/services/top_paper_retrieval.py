from typing import List, Dict
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def top_retrieve_paper(title: str, abstract: str, related_papers: List[Dict], top_k: int = 10) -> List[Dict[str,str]]:
    '''
    Retrieve the top 10 related papers based on the title and abstract of a given paper.
    '''
    if not related_papers:
        return []
    
    # Generate embeddings for the title and abstract
    query = f"{title.strip()} {abstract.strip()}"

    query_embedding = model.encode(query, convert_to_tensor=True)

    # Prepare the contents of the related papers for embedding

    paper_contents = []

    for paper in related_papers:
        paper_title = paper.get('title', '').strip()
        paper_abstract = paper.get('summary', '').strip()
        paper_contents.append(f"{paper_title} {paper_abstract}")

    paper_embeddings = model.encode(paper_contents, convert_to_tensor=True)

    # Compute cosine similarities

    cosine_scores = util.cos_sim(query_embedding, paper_embeddings)[0]

    top_indices = cosine_scores.topk(k=min(top_k, len(related_papers))).indices

    top_papers = []
    
    for index in top_indices:
        paper_title = related_papers[index]['title']
        paper_abstract = related_papers[index]['summary']
        paper_link = related_papers[index]['links']
    
        top_papers.append({
            'title': paper_title.strip(),
            'abstract': paper_abstract.strip(),
        })

    return top_papers

