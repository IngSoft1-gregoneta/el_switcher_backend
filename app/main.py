# FastApi
# Default query parameters
from typing import Union

# Unique id
from uuid import UUID, uuid4

from fastapi import (
    FastAPI,
    HTTPException,
    Response,
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
from models.visible_match import *
from room_handler import LeaveResult, RoomHandler

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
    return str(uuid4())


@app.get("/room/{room_id}")
async def get_room_data(
    room_id: UUID,
) -> Union[RoomOut, dict]:
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
    "/rooms/join/{room_id}/{user_id}",
    response_model=bool,
    status_code=status.HTTP_202_ACCEPTED,
)
async def join_room_endpoint(
    room_id: UUID,
    user_id: UUID,
    room_join: RoomJoin,
) -> bool:
    password = room_join.password
    player_name = room_join.player_name
    print(player_name)
    try:
        result = await room_handler.join_room(room_id, player_name, user_id, password)
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
    response_model=bool,
    status_code=status.HTTP_202_ACCEPTED,
)
async def leave_room_endpoint(
    room_id: UUID, player_name: str, user_id: UUID, response: Response
) -> bool:
    try:
        result = await room_handler.leave_room(room_id, player_name, user_id)
        try:
            if result == LeaveResult.DESTROYED:
                await manager.destroy_room(room_id)
            if result == LeaveResult.LEFT:
                await manager.leave(room_id, user_id)
            if result == LeaveResult.ERROR:
                response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
                return False
        except Exception as e:
            print(e)
            response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            return False
        return True
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )


# endopint to create a match
@app.post(
    "/matchs/create_match/{match_id}/{owner_name}", status_code=status.HTTP_201_CREATED
)
async def create_match_endpoint(match_id: UUID, owner_name: str):
    match = await match_handler.create_match(match_id, owner_name, manager)
    await manager.broadcast_by_room(match_id, "MATCH")
    await manager.broadcast("LISTA")
    return match


@app.get("/matchs/{match_id}")
async def get_match_data(
    match_id: UUID,
) -> Union[MatchOut, dict]:
    return await match_handler.get_match_by_id(match_id)


@app.put(
    "/matchs/leave_match/{match_id}/{player_name}/{user_id}",
    response_model=Union[MatchOut, str],
    status_code=status.HTTP_202_ACCEPTED,
)
async def leave_match(
    match_id: UUID,
    player_name: str,
    user_id: UUID,
) -> Union[MatchOut, str]:
    try:
        result = await match_handler.leave_match(player_name, match_id, manager)
        try:
            await manager.leave_match(match_id, user_id)
        except Exception as e:
            print(e)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.get("/matchs/visible_match/{match_id}/{player_name}")
async def get_match_data_by_player(
    match_id: UUID, player_name: str
) -> VisibleMatchData:
    try:
        visible_match = await match_handler.get_visible_data_by_player(
            match_id, player_name, manager
        )
        return visible_match
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.put("/matchs/end_turn/{match_id}/{player_name}")
async def end_turn(match_id: UUID, player_name: str):
    try:
        match = await match_handler.end_turn(match_id, player_name, manager)
        await manager.broadcast_by_room(match_id, "MATCH")
        return match
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.put("/parcial_move/{match_id}/{player_name}/{card_index}/{x1}/{y1}/{x2}/{y2}")
async def parcial_mov(
    match_id: UUID,
    player_name: str,
    card_index: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
):
    print("0")
    try:
        print("1")
        await match_handler.do_parcial_mov(
            match_id, player_name, card_index, x1, y1, x2, y2
        )
        print("2")
        await manager.broadcast_by_room(match_id, "MATCH")
        print("3")
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.put("/revert_movement/{match_id}/{player_name}")
async def revert_movement(match_id: UUID, player_name: str):
    try:
        await match_handler.revert_mov(match_id, player_name)
        await manager.broadcast_by_room(match_id, "MATCH")
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.put("/discard_figure/{match_id}/{player_name}/{card_index}/{x}/{y}")
async def discard_figure(
    match_id: UUID, player_name: str, card_index: int, x: int, y: int
):
    try:
        await match_handler.discard_fig(match_id, player_name, card_index, x, y)
        await manager.broadcast_by_room(match_id, "MATCH")
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.put(
    "/block_figure/{match_id}/{player_name}/{other_player_name}/{card_index}/{x}/{y}"
)
async def block_figure(
    match_id: UUID,
    player_name: str,
    other_player_name: str,
    card_index: int,
    x: int,
    y: int,
):
    try:
        await match_handler.block_fig(
            match_id, player_name, other_player_name, card_index, x, y
        )
        await manager.broadcast_by_room(match_id, "MATCH")
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
