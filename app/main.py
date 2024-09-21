# FastApi
from fastapi import Cookie, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
# Unique id
from uuid import uuid4
# Default query parameters
from typing import Annotated, Optional
# Data from manager.py
from manager import manager
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# data, methods and classes of a room
from models.room import *
from models.match import *
from typing import Union

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = manager.ConnectionManager()
# Aca podriamos asignar el mismo socket para el grupo de jugadores en la misma partida?
user_socket = {}

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, user_id: Annotated[str | None, Cookie()] = None
):
   # logger.debug(user_id)
    await manager.connect(websocket)
    user_socket[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
@app.get("/get_id")
def get_id():
    return uuid4()

# Define endline to create a new room
@app.post("/rooms/create_room",
          response_model=RoomOut,
          status_code=status.HTTP_201_CREATED)
async def create_room(new_room: RoomIn) -> RoomOut:
    repo = RoomRepository()
    if new_room.players_expected < 2 or new_room.players_expected > 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong amount of players")
    # Verificar si el nombre de la sala ya existe en la base de datos
    existing_room = repo.check_for_names(new_room.room_name)
    if existing_room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room name already exists")
    
    try:
        
        result = repo.create_room(new_room)
       
        return result

    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
# endpoint for room leave request 
@app.put("/rooms/leave",
        response_model=Union[RoomOut,dict],
        status_code=status.HTTP_202_ACCEPTED)
async def leave_room_endpoint(room_id: int, player_name: str):
    repo = RoomRepository()
    try:
        room = repo.get_room_by_id(room_id)
        if room == None:
            return {"message": "Room not found"}
        if not(player_name in room.players_names):
            return {"message": "There is not such a player"}
        repo.update_players(room.players_names,player_name,room_id,"remove")
        return repo.get_room_by_id(room_id)
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@app.put("/rooms/join",
        response_model=Union[RoomOut,dict],
        status_code=status.HTTP_202_ACCEPTED)
async def join_room_endpoint(room_id: int, player_name: str):
    repo = RoomRepository()
    try:
        room = repo.get_room_by_id(room_id)

        if room is None:
            return {"message": "Room not found"}

        if len(room.players_names) == room.players_expected:
            return {"message": "Room is full"}
        
        if player_name in room.players_names:
            return {"message": "The name already exists, choose another"}
        
        repo.update_players(room.players_names,player_name,room_id,"add")
        return repo.get_room_by_id(room_id)
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

# Define endpoint to get rooms list
@app.get("/rooms/")
async def get_rooms():
    repo = RoomRepository()
    try:
        return repo.get_rooms()
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

# Define endpoint to create a room
@app.post("/matchs/create_match",
          status_code=status.HTTP_201_CREATED)
async def create_match(matchIn: MatchIn):
    repo = MatchRepository()
    try:
        match = MatchOut(matchIn.room_id)
        repo.create_match(match)
        return repo.get_match_by_id(matchIn.room_id).model_dump(mode="json")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: {e}")
