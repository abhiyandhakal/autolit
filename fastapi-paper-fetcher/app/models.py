from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    keyword: str

class PaperInfo(BaseModel):
    title: str
    authors: List[str]
    link: Optional[str]

class SearchResults(BaseModel):
    results: dict[str, List[PaperInfo]]  # API name as key, list of papers as value
