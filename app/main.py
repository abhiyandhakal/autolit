from fastapi import FastAPI
from dotenv import load_dotenv

from app.services.keywords import keyword_gen
from app.models.keyword import KeywordsReqBody
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
