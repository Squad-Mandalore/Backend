from fastapi.testclient import TestClient
from src.main import app

# Description: This file contains the test variables that are used in the test cases

client = TestClient(app)

class TestVariables():
    HEADERS: dict = {'content-type': 'application/json'}
    BASEURL: str = 'http://127.0.0.1:8000'
    EXAMPLE_PASSWORD: dict = {"password": "Go is the GOAT"}
