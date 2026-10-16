from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#  TEST HOME API

def test_home():
    response = client.get("/")

    #  STATUS CODE CHECK
    assert response.status_code == 200

    # RESPONSE DATA CHECK
    assert response.json() == {"message": "Welcome to the FastAPI application!"}

# TEST ADD API

def test_add():
    response = client.get("add?a=96&b=4")

    # STATUS CODE CHECK
    assert response.status_code == 200

    # RESPONSE DATA CHECK
    assert response.json() == {"result": 100}