from typing import List
from pydantic import BaseModel

class FormEntity(BaseModel):
    entity: str
    synonyms: List[str]


class FormEntityType(BaseModel):
    entity_type: str
    keywords: List[str]
    isNumeric: bool
    entities: List[FormEntity]


class FormIntent(BaseModel):
    intent: str
    examples: List[str]
    entity_types: List[FormEntityType]