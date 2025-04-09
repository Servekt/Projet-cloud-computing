import json
from app.app import app

def test_news_endpoint():
    client = app.test_client()
    response = client.get("/api/news")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_events_endpoint():
    client = app.test_client()
    response = client.get("/api/events")
    assert response.status_code == 200
    assert isinstance(response.json, list)
