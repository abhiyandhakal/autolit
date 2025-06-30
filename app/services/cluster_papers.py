from typing import Dict, List
import hdbscan
from sentence_transformers import SentenceTransformer, util
import json
from collections import defaultdict
from sklearn.preprocessing import StandardScaler

from app.services.keywords import keyword_gen
from app.services.paper_retrieval import retrieve_papers

model = SentenceTransformer('all-MiniLM-L6-v2')

clusterer = hdbscan.HDBSCAN()

def cluster_papers(papers: List[Dict], min_cluster_size: int = 2):
    if not papers:
        return {}

    # Prepare embeddings
    texts = [
        f"{paper.get('title', '').strip()} {paper.get('summary', '').strip()}"
        for paper in papers
    ]
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Normalize embeddings
    embeddings = StandardScaler().fit_transform(embeddings)

    # Run HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean')
    cluster_labels = clusterer.fit_predict(embeddings)
    print("cluster labels", cluster_labels)

    # Organize papers by cluster
    clustered = defaultdict(list)
    for paper, label in zip(papers, cluster_labels):
        clustered[label].append(paper)

    return clustered


# Test data
title = "Feasibility of Artificial Intelligence Driven Analysis in the Context of Nepalese Legal System"
abstract = "We proposed an innovative solution through an Artificial Intelligence driven legal analysis customized to the utility of the Nepalese legal context. Using advanced machine learning (ML) models and Retrieval-Augmented Generation (RAG) techniques, the research provides legal insights, streamlines judicial processes, and enhances accessibility to legal information. The legal documents were processed to convert into JSON format, and then to convert into vector data. GPT-4o was used for query expansion and response generation, whereas text embeddings were generated through text-embedding-ada-002. Key features include efficient document retrieval and query expansion for enhanced search precision. The model performs well across different query types, achieving an 𝐹1 score of 0.797 for rule-recall, 0.857 for rhetorical understanding, and 0.875 for interpretation-based queries. This work marks a significant step towards integrating AI into the legal domain of Nepal."

keywords = keyword_gen(title, abstract)
papers_unfiltered = []
for keyword in keywords:
    papers_unfiltered = papers_unfiltered + retrieve_papers(keyword=keyword)

# Remove repeated
papers = []
seen_ids = set()
for paper in papers_unfiltered:
    if paper['id'] not in seen_ids:
        papers.append(paper)
        seen_ids.add(paper['id'])

print("papers count",len(papers))

# __import__('pprint').pprint(cluster_papers(papers))
clustered = cluster_papers(papers)
