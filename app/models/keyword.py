from pydantic import BaseModel

class KeywordsReqBody(BaseModel):
    title: str
    abstract: str
