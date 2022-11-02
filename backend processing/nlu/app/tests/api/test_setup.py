#!/usr/bin/env python3
from fastapi.testclient import TestClient
from app.main import app
from app.services.engine_manager import EngineName

client = TestClient(app)


def test_setup():
    for item in EngineName:
        response = client.put(f"/infer/setup/{item.value}")
        assert response.status_code == 200
        assert response.json() == {
            "model": item.value
        }


def test_setup_no_token():
    response = client.put("/infer/setup/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found"
    }


def test_setup_bad_token():
    path_param = "rasa"
    response = client.put(f"/infer/setup/{path_param}")
    assert response.status_code == 422
