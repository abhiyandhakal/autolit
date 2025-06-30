import time
from fastapi import FastAPI
from dotenv import load_dotenv

from app.services.paper_retrieval import retrieve_papers
from app.services.keywords import keyword_gen
from app.models.keyword import KeywordsReqBody
from app.services.top_paper_retrieval import top_retrieve_paper
load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post(
    "/keywords", 
    description="Generate keywords from abstract and title",
)
async def keywords(body: KeywordsReqBody):
    return keyword_gen(title=body.title, abstract=body.abstract)

@app.post(
    "/related-works",
    description="Get related works",
)
async def related_works(body: KeywordsReqBody):
    keywords = keyword_gen(title=body.title, abstract=body.abstract)
    papers = []
    for keyword in keywords:
        papers = papers + retrieve_papers(keyword=keyword)

    return papers

@app.post(
    "/top-related-works",
    description="Get the top 10 related works from the given sets of keywords",
)

async def top_related_works(body: KeywordsReqBody):
    keywords = keyword_gen(title=body.title, abstract=body.abstract)
    papers = []
    for keyword in keywords:
        papers = papers + retrieve_papers(keyword=keyword)
    
    best_related_papers = top_retrieve_paper(title=body.title, abstract=body.abstract, related_papers=papers, top_k=10)
        
    return best_related_papers
