from html import entities
from typing import List
from pydantic import BaseModel
from app.schemas.entity import Entity

class EntityType(BaseModel):
    entity_type: str
    keywords: List[str]
    entities: List[Entity]

    