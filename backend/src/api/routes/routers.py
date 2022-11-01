from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from api.routes.extraction.OwnKeywordExtraction import *
from api.routes.extraction.TextRanking import *

route = APIRouter(prefix="/analysis")

@route.get("/own-keyword-extraction", response_description="Own Keyword Extraction")
async def own_keyword_extraction(request: Request):
    return keyword_extraction()

@route.get("/top-freq-keywords", response_description="Top Frequent Keywords")
async def top_freq_keywords(request: Request):
    return freq_text_ranking()

@route.get("/top-operator-keywords", response_description="Top Frequent Operator Keywords")
async def top_operator_keywords(request: Request):
    return operator_text_ranking()

@route.get("/top-caller-keywords", response_description="Top Frequent Caller Keywords")
async def top_caller_keywords(request: Request):
    return caller_text_ranking()

@route.get("/get-types", response_description="List all types")
def list_types(request: Request):
    types = []
    for filter in request.app.database["filter"].find():
        # Note: Every items object must have a unique "id" property and "text" property to display on frontend
        types.append({"id":filter["id"], "text":filter["type"]})
    return types