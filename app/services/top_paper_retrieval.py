from typing import List, Dict
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_relevant_papers(title: str, abstract: str, related_papers: List[Dict]) -> List[Dict[str,str]]:
    '''
    Retrieve the top k related papers based on the title and abstract of a given paper.
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
    print("cosine_scores", cosine_scores)

    relevant_indices = (cosine_scores >= 0.6).nonzero(as_tuple=True)[0]
    relevant_papers = [related_papers[i] for i in relevant_indices.tolist()]

    return relevant_papers
