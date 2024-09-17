from fastapi.testclient import TestClient
from fastapi import status
from room import rooms
from typing import List
from main import app

from main import app

client = TestClient(app)

def test_endturn_basic():

    # Basic info to test
    room_id = 1
    room_name = "foo name"
    players_expected = 4
    players: List[str] = ["Braian", "Tadeo", "Yamil", "Grego"]
    is_active = True

    new_room_data = {"room_id": room_id,
                    "room_name": room_name,
                    "players_expected": players_expected,
                    "players": players,
                    "is_active": is_active}
    
    
    sent = client.post("/rooms/", json=new_room_data)
    assert sent.status_code == status.HTTP_201_CREATED

    response = client.get("/rooms/")
    assert response.status_code == status.HTTP_200_OK

    room_data = response.json()

    # Modifico la lista de jugadores
    end_turn_response = client.put(f"/match/?{room_id}/endturn/")
    assert end_turn_response.status_code == status.HTTP_200_OK
    # REVISAR incongruencia /rooms/ != /match/id/endturn/

    current_data = end_turn_response.json()
    assert "players" in current_data

    assert current_data["players"] != "Tadeo"
    

    
    
