from fastapi.testclient import TestClient
from fastapi import status
from room import *
from match import *
from typing import List
from main import app

from main import app

client = TestClient(app)

def test_addmatch():
    ROOMS.clear()
    MATCHS.clear()
    room_id = 1
    room_name = "Room 1"
    players_expected = 2
    players_names = ['Yamil','Tadeo']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    match = Match(match_id=room_id)
    MATCHS.append(match.model_dump())

def test_endturn_correctness():
    test_addmatch()
    match_id = 1
    match = get_match_by_id(match_id)

    previousT = check_turn(match)
    
    response = client.put(f"/match/?match_id={match_id}/endturn")
    assert response.status_code == status.HTTP_202_ACCEPTED

    nextT = check_turn(match)

    assert previousT != nextT
