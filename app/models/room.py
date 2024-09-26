import json
from typing import List

from config.repositorymanager import Room, Session
from pydantic import BaseModel, Field


class RoomIn(BaseModel):
    room_name: str
    players_expected: int
    owner_name: str


class RoomOut(BaseModel):
    room_id: int
    room_name: str
    players_expected: int
    players_names: List[str] = []
    owner_name: str
    is_active: bool = True


class RoomRepository:
    def create_room(self, new_room: RoomIn):
        db = Session()
        try:
            last_room = db.query(Room).order_by(Room.room_id.desc()).first()
            new_id = (last_room.room_id if last_room else 0) + 1

            roomOut = RoomOut(
                room_id=new_id,
                room_name=new_room.room_name,
                players_expected=new_room.players_expected,
                players_names=[new_room.owner_name],
                owner_name=new_room.owner_name,
                is_active=True,
            )

            roombd = Room(
                room_name=new_room.room_name,
                room_id=new_id,
                players_expected=new_room.players_expected,
                owner_name=new_room.owner_name,
                players_names=json.dumps(roomOut.players_names),
                is_active=True,
            )
            db.add(roombd)
            db.commit()
            return roomOut.model_dump()
        finally:
            db.close()

    # Fetch room by id or return None if the room was not found
    def get_room_by_id(self, room_id: int) -> RoomOut | None:
        db = Session()
        try:
            result = db.query(Room).filter(Room.room_id == room_id).one_or_none()
            if result:
                room = RoomOut(
                    room_id=result.room_id,
                    room_name=result.room_name,
                    players_expected=result.players_expected,
                    players_names=json.loads(result.players_names) or [],
                    owner_name=result.owner_name,
                    is_active=result.is_active,
                )
                return room
            return None
        finally:
            db.close()

    # Methods are: add, remove
    def update_players(
        self, players: List[str], player_name: str, room_id: int, method: str
    ):
        if method == "add":
            players.append(player_name)
        elif method == "remove" and player_name in players:
            players.remove(player_name)

        db = Session()
        try:
            db_room = db.query(Room).filter(Room.room_id == room_id).one()
            db_room.players_names = json.dumps(players)
            db.commit()
        finally:
            db.close()

    def get_rooms(self):
        db = Session()
        try:
            rooms = db.query(Room).all()

            return [
                RoomOut(
                    room_id=room.room_id,
                    room_name=room.room_name,
                    players_expected=room.players_expected,
                    players_names=json.loads(room.players_names) or [],
                    owner_name=room.owner_name,
                    is_active=room.is_active,
                ).model_dump()
                for room in rooms
            ]
        finally:
            db.close()

    def check_for_names(self, room_name: str):
        db = Session()
        try:
            return db.query(Room).filter(Room.room_name == room_name).first()
        finally:
            db.close()

    def delete(self, id):
        db = Session()

        try:
            todelete = db.query(Room).filter(Room.room_id == id).one_or_none()
            db.delete(todelete)
            db.commit()
        finally:
            db.close()

