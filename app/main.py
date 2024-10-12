# FastApi
# Default query parameters
from typing import Annotated, Any, Optional, Union

# Unique id
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status

# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware

# data, methods and classes of a room
from manager.manager import ConnectionManager
from match_handler import MatchHandler
from models.match import *
from models.room import *
from models.visible_match import *
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
    "/rooms/join/{room_id}/{player_name}/{user_id}",
    response_model=Union[RoomOut, dict],
    status_code=status.HTTP_202_ACCEPTED,
)
async def join_room_endpoint(room_id: UUID, player_name: str, user_id: UUID):
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
async def leave_room_endpoint(room_id: UUID, player_name: str, user_id: UUID):
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
@app.post("/matchs/create_match/{match_id}/{owner_name}", status_code=status.HTTP_201_CREATED)
async def create_match_endpoint(match_id: UUID, owner_name: str):
    match = await match_handler.create_match(match_id, owner_name)
    await manager.broadcast_by_room(match_id, "MATCH")
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
        result = await match_handler.leave_match(player_name, match_id)
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
            match_id, player_name
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
async def end_turn(match_id: UUID, player_name: str) -> MatchOut:
    try:
        match = await match_handler.end_turn(match_id, player_name)
        await manager.broadcast_by_room(match_id, "MATCH")
        return match
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
@app.get("/matchs/winner/{match_id}")
async def check_winner(
    match_id: UUID
    ) -> Union[str, None]:
    try:
        winner = await match_handler.check_winner(match_id)
        # await manager.broadcast_by_room(match_id, "MATCH")
        return winner
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {e}",
        ) 
        
    
@app.put("/use_movement_card/{match_id}/{player_name}")
async def use_movement_card(match_id: UUID, player_name: str, card_index: int):
    try:
        visible_movement = await match_handler.use_mov_card(match_id, player_name, card_index)
        return visible_movement
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    

# @app.post("/confirm_movement/{match_id}/{player_name}/{card_index}")
# async def confirm_movement(match_id: UUID, player_name: str, card_index: int):
#     match = match_repository.get_match_by_id(match_id)
#     player = match.get_player_by_name(player_name)
# 
#     if card_index < 0 or card_index >= len(player.mov_cards):
#         raise HTTPException(status_code=400, detail="Invalid card index")
#     
#     card = player.mov_cards[card_index]
# 
#     if not card.is_used:
#         raise HTTPException(status_code=400, detail="Cannot confirm a card that has not been used.")
# 
#     me = Me(match_id=match_id, player_name=player_name)
# 
#     try:
#         confirmed_card = me.confirm_movement_card(match_id, player_name, card)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
# 
#     return me