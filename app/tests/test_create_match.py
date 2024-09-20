from fastapi.testclient import TestClient
from fastapi import status
from main import app
from match import *
from room import * 

client = TestClient(app)

def test_match_2_players():
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
    matchIn = MatchIn(room_id=room_id)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() in MATCHS

def test_match_3_players():
    ROOMS.clear()
    MATCHS.clear()
    room_id = 2
    room_name = "Room 2"
    players_expected = 3
    players_names = ['Yamil','Tadeo', 'Facu']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    matchIn = MatchIn(room_id=room_id)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() in MATCHS

def test_match_4_players():
    ROOMS.clear()
    MATCHS.clear()
    room_id = 3
    room_name = "Room 3"
    players_expected = 4
    players_names = ['Yamil','Tadeo', 'Facu', 'Braian']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    matchIn = MatchIn(room_id=room_id)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() in MATCHS

def test_dup_match():
    matchIn = MatchIn(room_id=3)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() not in MATCHS

def test_no_full_match():
    MATCHS.clear()
    ROOMS.clear()
    room_id = 1
    room_name = "Room 1"
    players_expected = 4
    players_names = ['Yamil','Tadeo', 'Facu']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    matchIn = MatchIn(room_id=room_id)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() not in MATCHS
    ROOMS.clear()

def test_match_without_room():
    MATCHS.clear()
    ROOMS.clear()
    matchIn = MatchIn(room_id=1)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() not in MATCHS
    ROOMS.clear()

def test_match_a_player():
    MATCHS.clear()
    ROOMS.clear()
    room_id = 1
    room_name = "Room 1"
    players_expected = 1
    players_names = ['Yamil']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    matchIn = MatchIn(room_id=room_id)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() not in MATCHS

def test_match_5_player():
    MATCHS.clear()
    ROOMS.clear()
    room_id = 1
    room_name = "Room 1"
    players_expected = 5
    players_names = ['Yamil','Braian','Tadeo','Mou','Nico']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    matchIn = MatchIn(room_id=room_id)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() not in MATCHS
    ROOMS.clear()