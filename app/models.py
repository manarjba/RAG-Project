from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
