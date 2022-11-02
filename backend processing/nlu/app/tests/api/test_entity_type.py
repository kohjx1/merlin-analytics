#!/usr/bin/env python3
from typing import Optional, List
from fastapi.testclient import TestClient
import json
import urllib.parse

from app.main import app
from app.models.forms import FormEntityType
from app.models.forms_DAO import form_DAO
from app.api.dependencies.form_manager import get_entity_type_col

client = TestClient(app)

async def override_dependency(intent: Optional[str] = None) -> List[FormEntityType]:
    with open('app/tests/sample_entity_types.json', encoding="utf8") as f:
        # read json file as dict
        raw_entity_type_col = json.load(f)

        entity_type_col = []
        for doc in raw_entity_type_col:
            entity_type_col.append(form_DAO.cast_as_FormEntityType(doc))
        
        if intent is None:
            return entity_type_col
        
        with open('app/tests/sample_intents.json', encoding="utf8") as f_int:
            raw_intent_col = json.load(f_int)
            intent_col = []
            for doc in raw_intent_col:
                intent_col.append(form_DAO.cast_as_FormIntent(doc, entity_type_col))
                
            return form_DAO.access_entity_types_by_intent(intent_col, intent)

app.dependency_overrides[get_entity_type_col] = override_dependency


def test_entity_type_missing_text():
    response = client.get("/infer/entity-type/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found"
    }


def test_entity_type_without_intent():
    text = 'I am twenty four years old'
    encoded_text = urllib.parse.quote(text)

    response = client.get("/infer/entity-type/" + encoded_text)
    assert response.status_code == 200
    assert response.json() == [
        {
            'entity_type': 'age', 
            'keywords': ['years old'],
            'entities': [
                {'entity': '24', 'synonyms': ['twenty four']}
            ] 
        }
    ] 


def test_entity_type_with_intent():
    text = 'I am twenty four years old'
    encoded_text = urllib.parse.quote(text)

    response = client.get("/infer/entity-type/" + encoded_text + "?intent=fill_form_medical")
    assert response.status_code == 200
    assert response.json() == [
        {
            'entity_type': 'age', 
            'keywords': ['years old'],
            'entities': [
                {'entity': '24', 'synonyms': ['twenty four']}
            ] 
        }
    ] 