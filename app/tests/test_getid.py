from uuid import *

from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.room import *

client = TestClient(app)

def test_getid():
    response = client.get("/get_id")
    data = response.json()
    assert str(UUID(data)) == response.json()