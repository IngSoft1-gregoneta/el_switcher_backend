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
from match_handler import MatchHandler
from models.match import *
from models.room import *
from room_handler import RoomHandler

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

# instancia de RoomHandler para manejar la lógica de los endpoints de room
room_handler = RoomHandler()

match_handler = MatchHandler()


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
        return await room_handler.get_data_from_a_room(room_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# Define endpoint to get rooms list
@app.get("/rooms")
async def get_rooms():
    try:
        return await room_handler.get_all_rooms()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# endpoint for create room
@app.post(
    "/rooms/create_room/{user_id}",
    response_model=RoomOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_room_endpoint(new_room: RoomIn, user_id: UUID) -> RoomOut:
    try:
        result = await room_handler.create_room(new_room)
        # TODO: Sacar esto hacer mock
        try:
            await manager.create(result["room_id"], user_id)
        except Exception as e:
            print(e)
        return result
    except HTTPException as http_ex:
        raise http_ex
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.put(
    "/rooms/join/{room_id}/{player_name}/{user_id}",
    response_model=Union[RoomOut, dict],
    status_code=status.HTTP_202_ACCEPTED,
)
async def join_room_endpoint(room_id: int, player_name: str, user_id: UUID):
    try:
        result = await room_handler.join_room(room_id, player_name, user_id)
        try:
            await manager.join(room_id, user_id)
        except Exception as e:
            print(e)
        return result
    except HTTPException as http_exc:
        # si es una HTTPException, dejamos que pase como está
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# endpoint for room leave request
@app.put(
    "/rooms/leave/{room_id}/{player_name}/{user_id}",
    response_model=RoomOut | dict | None,
    status_code=status.HTTP_202_ACCEPTED,
)
async def leave_room_endpoint(room_id: int, player_name: str, user_id: UUID):
    try:
        result = await room_handler.leave_room(room_id, player_name, user_id)
        # Si es none es porq se destruyo la room
        try:
            if result == None:
                await manager.destroy_room(room_id)
            else:
                await manager.leave(room_id, user_id)
        except Exception as e:
            print(e)
        return result
    except HTTPException as http_exc:
        # si es una HTTPException, dejamos que pase como está
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# endopint to create a match
@app.post(
    "/matchs/create_match/{match_id}/{owner_name}", status_code=status.HTTP_201_CREATED
)
async def create_match_endpoint(matchIn: MatchIn, owner_name: str):
    return await match_handler.create_match(matchIn, owner_name)


@app.get("/matchs/{match_id}")
async def get_match_data(
    match_id: int,
) -> Union[MatchOut, dict]:  # union para que pueda devolver tanto MatchOut como un dict
    return await match_handler.get_match_by_id(match_id)


@app.put(
    "/matchs/leave_match/{match_id}/{player_name}/{user_id}",
    response_model=Union[MatchOut, str],
    status_code=status.HTTP_202_ACCEPTED,
)
async def leave_match(
    match_id: int,
    player_name: str,
    user_id: UUID,
) -> Union[MatchOut, str]:
    try:
        result = await match_handler.leave_match(player_name, match_id)
        try:
            await manager.leave(match_id, user_id)
        except Exception as e:
            print(e)
        return result
    except HTTPException as http_exc:
        # si es una HTTPException, dejamos que pase como está
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.put("/matchs/{match_id}/endturn", status_code=status.HTTP_202_ACCEPTED)
async def endturn(match_id: int):
    repo = MatchRepository()
    try:
        match = repo.get_match_by_id(match_id)
        next_turn(match)
        return {"message": "¡Próximo Turno!"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: {e}"
        )
