#!/usr/bin/env python3
from fastapi import FastAPI

from app.core.logging import configure_logging
from app.api.routers import entities, entity_types, intents, setup

configure_logging()

app = FastAPI()

app.include_router(setup.router)
app.include_router(intents.router)
app.include_router(entity_types.router)
app.include_router(entities.router)
