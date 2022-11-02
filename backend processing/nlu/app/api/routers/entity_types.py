#!/usr/bin/env python3
import sys, traceback
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas import EntityType
from app.models.forms import FormEntityType
from app.services.engine_manager import engine_manager
from app.api.dependencies.form_manager import get_entity_type_col

router = APIRouter(
    prefix="/infer/entity-type"
)

@router.get("/{text}", response_model=List[EntityType])
async def get_entity_types(
    text: str, 
    entity_type_col: List[FormEntityType] = Depends(get_entity_type_col)
) -> List[EntityType]:
    """
    Attempt to understand the entities in a text given an optional intent. 
    Returns the entity types and entities detected in the text.
    """
    try:
        entities = engine_manager.get_entity_types(text, entity_type_col)
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()      
        raise HTTPException(status_code=400, detail=traceback.format_exc().splitlines()[-1])

    return entities