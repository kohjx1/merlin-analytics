#!/usr/bin/env python3
from fastapi.testclient import TestClient
import json
import urllib.parse

from app.main import app
from app.models.forms import FormEntityType
from app.models.forms_DAO import form_DAO
from app.api.dependencies.form_manager import get_entity_type_doc

client = TestClient(app)

async def override_dependency(entity_type: str) -> FormEntityType:
    with open('app/tests/sample_entity_types.json', encoding="utf8") as f:
        # read json file as dict
        raw_entity_type_col = json.load(f)
        entity_type_col = []
        for doc in raw_entity_type_col:
            entity_type_col.append(form_DAO.cast_as_FormEntityType(doc))
        
        return form_DAO.access_entity_type(entity_type_col, entity_type)

app.dependency_overrides[get_entity_type_doc] = override_dependency


def test_entity_missing_text():
    response = client.get("/infer/entity/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found"
    }


def test_entity_missing_query():
    text = 'I am twenty four years old'
    encoded_text = urllib.parse.quote(text)

    response = client.get("/infer/entity/" + encoded_text)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                'loc': ['query', 'entity_type'], 
                'msg': 'field required', 
                'type': 'value_error.missing'
            }
        ]
    }


def test_entity_wrong_entity_type():
    text = 'I am twenty four years old'
    encoded_text = urllib.parse.quote(text)

    response = client.get("/infer/entity/" + encoded_text + "?entity_type=foo")
    assert response.status_code == 200
    assert response.json() == []


def test_single_entity():
    text = 'I am twenty four years old'
    encoded_text = urllib.parse.quote(text)

    response = client.get("/infer/entity/" + encoded_text + "?entity_type=age")
    assert response.status_code == 200
    assert response.json() == [
        {'entity': '24', 'synonyms': ['twenty four']}
    ] 


def test_multiple_entities():
    text = 'I am feeling feverish, I think the fever started last night. I am also coughing.'
    encoded_text = urllib.parse.quote(text)

    response = client.get("/infer/entity/" + encoded_text + "?entity_type=physical_symptoms")
    assert response.status_code == 200
    assert response.json() == [
        {'entity': 'Fever', 'synonyms': ["fever", "feverish"]},
        {'entity': 'Cough', 'synonyms': ["coughing"]}
    ] 