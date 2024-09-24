# FastApi
# Default query parameters
from typing import Annotated, Optional, Union

# Unique id
from uuid import UUID, uuid4

from fastapi import (
    Cookie,
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)

# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware

# Data from manager.py
from manager.manager import ConnectionManager
from match import *

# data, methods and classes of a room
from room import *

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: UUID):
    # logger.debug(user_id)
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)


# Define endpoint to get rooms list
@app.get("/rooms")
async def get_rooms():
    try:
        return ROOMS
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.get("/room/{room_id}")
async def get_room_data(
    room_id: int,
) -> Union[RoomOut, dict]:  # union para que pueda devolver tanto RoomOut como un dict
    try:
        room = get_room_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return room

    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.get("/get_id")
def get_id():
    return uuid4()


# Define endline to create a new room
@app.post(
    "/rooms/create_room/{user_id}",
    response_model=RoomOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_room(new_room: RoomIn, user_id: UUID) -> RoomOut:
    if new_room.players_expected < 2 or new_room.players_expected > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong amount of players"
        )
    for room in ROOMS:
        if room["room_name"] == new_room.room_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room name already exists",
            )

    try:
        last_id = ROOMS[-1]["room_id"] if ROOMS else 0
        new_id = last_id + 1

        # Create a new room dict
        roomOut = RoomOut(
            room_id=new_id,
            room_name=new_room.room_name,
            players_expected=new_room.players_expected,
            players_names=[new_room.owner_name],
            owner_name=new_room.owner_name,
            is_active=True,
        )

        ROOMS.append(roomOut.model_dump())

        manager.bind_room(room_id=new_id, user_id=user_id)
        await manager.broadcast_not_playing("LISTA")

        return roomOut.model_dump()

    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# Define endpoint to create a room
@app.post("/matchs/create_match", status_code=status.HTTP_201_CREATED)
async def create_match(matchIn: MatchIn):
    try:
        match = Match(matchIn.room_id)
        MATCHS.append(match.model_dump(mode="json"))
        return match.model_dump(mode="json")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: {e}"
        )


# endpoint for join room
@app.put(
    "/rooms/join/{room_id}/{player_name}/{user_id}",
    response_model=Union[RoomOut, dict],
    status_code=status.HTTP_202_ACCEPTED,
)
async def join_room_endpoint(
    room_id: int, player_name: str, user_id: UUID
) -> Union[RoomOut, dict]:  # union para que pueda devolver tanto RoomOut como un dict
    try:
        room = get_room_by_id(room_id)

        if room is None:
            print(1)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if len(room["players_names"]) >= room["players_expected"]:
            print(2)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Room is full"
            )

        # verificar si el jugador ya está en la sala
        if player_name in room["players_names"]:
            print(3)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Player name is already on the room",
            )

        # añadir el jugador a la sala
        room["players_names"].append(player_name)

        # crear una instancia de RoomOut con los datos actualizados
        roomOut = RoomOut(
            room_id=room["room_id"],
            room_name=room["room_name"],
            players_expected=room["players_expected"],
            players_names=room["players_names"],  # todos los jugadores actuales
            owner_name=room["owner_name"],
            is_active=room["is_active"],
        )

        try:
            # TODO:  ENUMS PARA MANAGER, o mejor encargarse todo el la clase
            manager.bind_room(room_id, user_id)
            await manager.broadcast_not_playing("LISTA")
            await manager.broadcast_by_room(room_id, "ROOM")
        except Exception as e:
            print("ERROR JOIN ", e)

        return roomOut.model_dump()

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# endpoint for room leave request
@app.put("/rooms/leave/{room_id}/{player_name}/{user_id}")
async def leave_room_endpoint(room_id: int, player_name: str, user_id: UUID):
    try:
        room = get_room_by_id(room_id)

        if room == None:
            return {"message": "Room not found"}
        if not (player_name in room["players_names"]):
            return {"message": "There is not such a player"}

        room["players_names"].remove(player_name)

        try:
            manager.unbind_room(room_id, user_id)
            await manager.broadcast_not_playing("LISTA")
            await manager.broadcast_by_room(room_id, "ROOM")
        except Exception as e:
            print("ERROR LEAVE ", e)
        return {"message": f"The player {player_name} has left the room {room_id}"}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
