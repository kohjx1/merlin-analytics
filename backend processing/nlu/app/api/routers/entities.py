#!/usr/bin/env python3
import sys, traceback
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas import Entity
from app.models.forms import FormEntityType
from app.services.engine_manager import engine_manager
from app.api.dependencies.form_manager import get_entity_type_doc

router = APIRouter(
    prefix="/infer/entity"
)

@router.get("/{text}", response_model=List[Entity])
async def get_entities(
    text: str, 
    entity_type_doc: FormEntityType = Depends(get_entity_type_doc)
) -> List[Entity]:
    """
    Attempt to understand the entities in a text given an optional intent. 
    Returns the entity types and entities detected in the text.
    """
    try:
        entities = engine_manager.get_entities(text, entity_type_doc)
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()      
        raise HTTPException(status_code=400, detail=traceback.format_exc().splitlines()[-1])

    return entities