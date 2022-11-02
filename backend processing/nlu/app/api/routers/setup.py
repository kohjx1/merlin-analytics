#!/usr/bin/env python3
from fastapi import APIRouter
from typing import Dict

from app.services.engine_manager import engine_manager, EngineName

router = APIRouter(prefix="/infer/setup")

@router.put("/{engine_name}")
async def choose_engine(
    engine_name: EngineName
) -> Dict[str, str]:
    """
    Choose the NLU model to be used 
    """
    engine_manager.choose_engine(engine_name)
    return {"model": engine_manager.engine_name}