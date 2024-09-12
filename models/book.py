from pydantic import BaseModel
from typing import List



class Book(BaseModel):
    id: int
    title: str
    description: str
    pages: int
    authors: List[str]



