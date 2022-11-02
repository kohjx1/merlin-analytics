from typing import List
from pydantic import BaseModel
from app.schemas.entity_type import EntityType

class Intent(BaseModel):
    intent: str
    examples: List[str]
    entity_types: List[EntityType]