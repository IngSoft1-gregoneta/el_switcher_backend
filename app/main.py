# FastApi
# Default query parameters
from typing import Annotated, Any, Optional, Union

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

# data, methods and classes of a room
from manager.manager import ConnectionManager
from models.match import *
from models.room import *

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


@app.get("/get_id")
def get_id():
    return uuid4()


@app.get("/room/{room_id}")
async def get_room_data(
    room_id: int,
) -> Union[RoomOut, dict]:  # union para que pueda devolver tanto RoomOut como un dict
    try:
        repo = RoomRepository()
        room = repo.get_room_by_id(room_id)
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


# Define endpoint to get rooms list
@app.get("/rooms")
async def get_rooms():
    repo = RoomRepository()
    try:
        return repo.get_rooms()
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# Define endline to create a new room
@app.post(
    "/rooms/create_room/{user_id}",
    response_model=RoomOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_room(
    new_room: RoomIn, user_id: UUID
) -> RoomOut | dict[str, Any]:  # TODO: Porq no volver RoomOut directamente?? Se puede ?
    repo = RoomRepository()
    if new_room.players_expected < 2 or new_room.players_expected > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong amount of players"
        )
    # Verificar si el nombre de la sala ya existe en la base de datos
    existing_room = repo.check_for_names(new_room.room_name)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Room name already exists"
        )

    try:
        result = repo.create_room(new_room)
        # TODO: Hacer un mock de WS para los test, asi no dejamos este try horrible
        try:
            manager.bind_room(result["room_id"], user_id)
            await manager.broadcast_not_playing("LISTA")
        except Exception as e:
            print("ERROR JOIN ", e)
        return result
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# TODO: This url change so i gess test must change
@app.put(
    "/rooms/join/{room_id}/{player_name}/{user_id}",
    response_model=Union[RoomOut, dict],
    status_code=status.HTTP_202_ACCEPTED,
)
async def join_room_endpoint(room_id: int, player_name: str, user_id: UUID):
    repo = RoomRepository()
    try:
        room = repo.get_room_by_id(room_id)

        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if len(room.players_names) == room.players_expected:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Room is full"
            )

        if player_name in room.players_names:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Player name is already on the room, choose another name",
            )
        repo.update_players(room.players_names, player_name, room_id, "add")
        try:
            # TODO:  ENUMS PARA MANAGER, o mejor encargarse todo el la clase
            manager.bind_room(room_id, user_id)
            await manager.broadcast_not_playing("LISTA")
            await manager.broadcast_by_room(room_id, "ROOM")
        except Exception as e:
            print("ERROR JOIN ", e)

        return repo.get_room_by_id(room_id)

    except HTTPException as http_exc:
        # si es una HTTPException, dejamos que pase como está
        raise http_exc


# endpoint for room leave request
@app.put(
    "/rooms/leave/{room_id}/{player_name}/{user_id}",
    response_model=Union[RoomOut, dict],
    status_code=status.HTTP_202_ACCEPTED,
)
async def leave_room_endpoint(room_id: int, player_name: str, user_id: UUID):
    repo = RoomRepository()
    try:
        room = repo.get_room_by_id(room_id)
        if room == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if not (player_name in room.players_names):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if player_name == room.owner_name: # si el owner abandona la sala, eliminar la sala
            repo.delete(room_id)
            return {"message": f"The owner {player_name} has left. Room {room_id} has been deleted."}
        try:
            manager.unbind_room(room_id, user_id)
            await manager.broadcast_not_playing("LISTA")
            await manager.broadcast_by_room(room_id, "ROOM")
        except Exception as e:
            print(f"Error al enviar el mensaje al socket: {e}")

        repo.update_players(room.players_names, player_name, room_id, "remove")
        return repo.get_room_by_id(room_id)

    except HTTPException as http_exc:
        # si es una HTTPException, dejamos que pase como está
        raise http_exc


# Define endpoint to create a room
@app.post("/matchs/create_match", status_code=status.HTTP_201_CREATED)
async def create_match(matchIn: MatchIn):
    repo = MatchRepository()
    try:
        match = MatchOut(matchIn.room_id)
        repo.create_match(match)
        return repo.get_match_by_id(matchIn.room_id).model_dump(mode="json")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: {e}")

@app.put("/matchs/{match_id}/endturn", status_code=status.HTTP_202_ACCEPTED)
async def endturn(match_id: int):
    repo = MatchRepository()
    try:
        match = repo.get_match_by_id(match_id)
        next_turn(match)
        return {'message': '¡Próximo Turno!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: {e}")