import json
from typing import List, Optional
from uuid import UUID, uuid1

from config.repositorymanager import Room, Session
from pydantic import BaseModel, Field


class RoomJoin(BaseModel):
    password: Optional[str]
    player_name: str


class RoomIn(BaseModel):
    room_name: str
    players_expected: int
    owner_name: str
    password: Optional[str]


class RoomOut(BaseModel):
    room_id: UUID
    room_name: str
    players_expected: int
    players_names: List[str] = []
    owner_name: str
    is_active: bool = True
    private: bool


class RoomRepository:
    def create_room(self, new_room: RoomIn):
        db = Session()
        try:
            new_id = uuid1()

            roomOut = RoomOut(
                room_id=new_id,
                room_name=new_room.room_name,
                players_expected=new_room.players_expected,
                players_names=[new_room.owner_name],
                owner_name=new_room.owner_name,
                password=new_room.password,
                private=(new_room.password != None),
                is_active=True,
            )

            roombd = Room(
                room_name=new_room.room_name,
                room_id=str(new_id),
                players_expected=new_room.players_expected,
                owner_name=new_room.owner_name,
                players_names=json.dumps(roomOut.players_names),
                password=new_room.password,
                private=(new_room.password != None),
                is_active=True,
            )
            db.add(roombd)
            db.commit()
            return roomOut.model_dump()
        finally:
            db.close()

    # Fetch room by id or return None if the room was not found
    def get_room_by_id(self, room_id: UUID) -> Optional[RoomOut]:
        db = Session()
        try:
            result = db.query(Room).filter(Room.room_id == str(room_id)).one_or_none()
            if result:
                return db_to_roomout(result)
            return None
        finally:
            db.close()

    # Methods are: add, remove
    def update_players(
        self, players: List[str], player_name: str, room_id: UUID, method: str
    ) -> bool:
        if method == "add":
            players.append(player_name)
        elif method == "remove" and player_name in players:
            players.remove(player_name)

        db = Session()
        try:
            db_room = db.query(Room).filter(Room.room_id == str(room_id)).one()
            db_room.players_names = json.dumps(players)
            db.commit()
            return True
        finally:
            db.close()

    def get_rooms(self):
        db = Session()
        try:
            rooms = db.query(Room).all()
            rooms_out = []
            for room in rooms:
                print(room.password)
                rooms_out.append(db_to_roomout(room).model_dump())
            return rooms_out
        finally:
            db.close()

    def verify_password(self, password: Optional[str], room_id: UUID) -> bool:
        db = Session()
        try:
            result = db.query(Room).filter(Room.room_id == str(room_id)).one_or_none()
            return result.password == password
        finally:
            db.close()

    def check_for_names(self, room_name: str):
        db = Session()
        try:
            return db.query(Room).filter(Room.room_name == room_name).first()
        finally:
            db.close()

    def delete(self, room_id: UUID) -> bool:
        db = Session()

        try:
            todelete = db.query(Room).filter(Room.room_id == str(room_id)).one_or_none()
            db.delete(todelete)
            db.commit()
            return True
        finally:
            db.close()

    def delete_rooms(self):
        db = Session()
        try:
            db.query(Room).delete()
            db.commit()
        finally:
            db.close()


def db_to_roomout(room) -> RoomOut:
    return RoomOut(
        room_id=room.room_id,
        room_name=room.room_name,
        players_expected=room.players_expected,
        players_names=json.loads(room.players_names) or [],
        owner_name=room.owner_name,
        private=room.private,
        is_active=room.is_active,
    )
