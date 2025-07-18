from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import matplotlib.pyplot as plt
import numpy as np

def retrieve_relevant_papers_tfidf(title: str, abstract: str, related_papers: List[Dict]) -> List[Dict[str,str]]:
    '''
    Retrieve top related papers using TF-IDF + Cosine Similarity.
    '''
    if not related_papers:
        return []

    # Combine query and documents
    query = f"{title.strip()} {abstract.strip()}"

    paper_contents = []
    for paper in related_papers:
        paper_title = paper.get('title', '').strip()
        paper_abstract = paper.get('summary', '').strip()
        paper_contents.append(f"{paper_title} {paper_abstract}")

    all_texts = [query] + paper_contents  # Query goes first

    # Create TF-IDF vectorizer and fit
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Compute cosine similarity (query vs each document)
    cosine_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Plot histogram
    plt.figure(figsize=(8, 5))
    plt.hist(cosine_scores, bins=20, color='lightgreen', edgecolor='black')
    plt.title("TF-IDF Cosine Similarity Distribution")
    plt.xlabel("Cosine Similarity")
    plt.ylabel("Number of Papers")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    print(cosine_scores)

    # Use IQR method
    q1 = np.quantile(cosine_scores, 0.25)
    q3 = np.quantile(cosine_scores, 0.75)
    iqr = q3 - q1
    threshold = q3 + 0.5 * iqr
    print("Threshold:", threshold)

    # Select relevant papers
    relevant_indices = np.where(cosine_scores >= threshold)[0]
    relevant_papers = [related_papers[i] for i in relevant_indices.tolist()]
    return relevant_papers

top_papers = retrieve_relevant_papers(title, abstract, papers)
print("papers count", len(top_papers))
