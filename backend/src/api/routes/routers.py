from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from api.routes.extraction.OwnKeywordExtraction import *
from api.routes.extraction.TextRanking import *

route = APIRouter(prefix="/analysis")

@route.get("/own-keyword-extraction", response_description="Own Keyword Extraction")
async def own_keyword_extraction():
    return keyword_extraction()

@route.post("/top-freq-keywords", response_description="Top Frequent Keywords")
async def top_freq_keywords(filter = Body()):
    return freq_text_ranking(int(filter))

@route.post("/top-operator-keywords", response_description="Top Frequent Operator Keywords")
async def top_operator_keywords(filter = Body()):
    return operator_text_ranking(int(filter))

@route.post("/top-caller-keywords", response_description="Top Frequent Caller Keywords")
async def top_caller_keywords(filter = Body()):
    return caller_text_ranking(int(filter))

@route.get("/get-types", response_description="List all types")
def list_types(request: Request):
    types = []
    for filter in request.app.database["filter"].find():
        # Note: Every items object must have a unique "id" property and "text" property to display on frontend
        types.append({"id":filter["id"], "text":filter["type"]})
    return types