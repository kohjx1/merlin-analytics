#!/usr/bin/env python3
from typing import List, Optional
from fastapi.testclient import TestClient
import json
import urllib.parse

from app.main import app
from app.models.forms import FormIntent
from app.models.forms_DAO import form_DAO
from app.api.dependencies.form_manager import get_intent_col

client = TestClient(app)

async def override_dependency(context: Optional[str] = None) -> List[FormIntent]:
    with open('app/tests/sample_intents.json', encoding="utf8") as f_intent:
        # read json file as dict
        raw_intents_col = json.load(f_intent)
        intents_col = []
        for doc in raw_intents_col:
            if context in doc["context"] or context is None:
                intents_col.append(doc)

        with open('app/tests/sample_entity_types.json', encoding="utf8") as f_entity_type:
            # read json file as dict
            raw_entity_type_col = json.load(f_entity_type)
            entity_type_col = []
            for doc in raw_entity_type_col:
                entity_type_col.append(form_DAO.cast_as_FormEntityType(doc))
            result = []
            for doc in intents_col:
                result.append(form_DAO.cast_as_FormIntent(doc, entity_type_col))

            return result

app.dependency_overrides[get_intent_col] = override_dependency


def test_intent_missing_text():
    response = client.get("/infer/intent/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found"
    }


def test_intent_without_context():
    text = 'Hi, there was an explosion at my house!'
    encoded_text = urllib.parse.quote(text)
    response = client.get("/infer/intent/" + encoded_text)
    assert response.status_code == 200 
    assert response.json() == [{
        'intent': 'get_form_type', 
        'examples': [],
        'entity_types': [
            {
                'entity_type': 'form_type', 
                'keywords': [], 
                'entities': [
                    {'entity': 'fire', 'synonyms': ['explosion']}
                ]
            }
        ]
    }] 


def test_intent_with_context():
    text = 'The fire is in the carpark'
    encoded_text = urllib.parse.quote(text)
    response = client.get("/infer/intent/" + encoded_text + "?context=fire")
    assert response.status_code == 200 
    assert response.json() == [{
        'intent': 'fill_form_fire', 
        'examples': [],
        'entity_types': [
            {
                'entity_type': 'fire_premise', 
                'keywords': [], 
                'entities': [
                    {'entity': 'Carpark Fire', 'synonyms': ['carpark']}
                ]
            }
        ]
    }] 

