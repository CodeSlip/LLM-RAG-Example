from fastapi.testclient import TestClient

from sechallenge.api import app


def test_hello():
    with TestClient(app) as client:
        response = client.get("/hello?name=Reba")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Reba!"}
        assert client.get("/hello").json() == {"message": "Hello Wilson!"}
