#!/usr/bin/env python3
import sys, traceback
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas import Intent
from app.models.forms import FormIntent
from app.services.engine_manager import engine_manager
from app.api.dependencies.form_manager import get_intent_col

router = APIRouter(
    prefix="/infer/intent"
)

@router.get("/{text}", response_model=List[Intent])
async def get_intents(
    text: str, 
    intent_col: List[FormIntent] = Depends(get_intent_col)
) -> List[Intent]:
    """
    Attempt to understand the intent of a text given an optional context. 
    Returns the intents, entity types and entities detected in the text.
    """
    try:
        intents = engine_manager.get_intents(text, intent_col)
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()      
        raise HTTPException(status_code=400, detail=traceback.format_exc().splitlines()[-1])

    return intents