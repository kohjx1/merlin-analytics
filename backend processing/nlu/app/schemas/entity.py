from typing import List
from pydantic import BaseModel


class Entity(BaseModel):
    entity: str
    synonyms: List[str]

