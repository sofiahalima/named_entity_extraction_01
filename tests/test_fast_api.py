from fastapi.testclient import TestClient
from app.service.main import app

client = TestClient(app)


def test_post_ner_bert():
    response = client.post("/ner?use_bert=true", json={"text": "Barack Obama visited Berlin."})
    assert response.status_code == 200
    result = response.json()
    assert "entities" in result
    assert any(ent["label"] in ["PER", "LOC", "GPE"] for ent in result["entities"])


def test_post_ner_spacy():
    response = client.post("/ner?use_bert=false", json={"text": "Barack Obama visited Berlin."})
    assert response.status_code == 200
    result = response.json()
    assert "entities" in result
