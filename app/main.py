# FastApi
from fastapi import FastAPI, HTTPException, status
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# data, methods and classes of a room
from room import *
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

# endpoint for join room
@app.put("/rooms/join",
         response_model=Union[RoomOut,dict],
         status_code=status.HTTP_202_ACCEPTED)
def join_room_endpoint(player_name: str, room_id: int) -> Union[RoomOut, dict]: # union para que pueda devolver tanto RoomOut como un dict
    try:
        room = get_room_by_id(room_id)

        if room is None:
            return {"message": "Room not found"}
        
        if len(room["players_names"]) >= room["players_expected"]:
            return {"message": "Room is full"}

        # verificar si el jugador ya está en la sala
        if player_name in room["players_names"]:
            return {"message": "The name already exists, choose another"}

        # añadir el jugador a la sala
        room["players_names"].append(player_name)

        # crear una instancia de RoomOut con los datos actualizados
        roomOut = RoomOut(
            room_id=room["room_id"],
            room_name=room["room_name"],
            players_expected=room["players_expected"],
            players_names=room["players_names"],  # todos los jugadores actuales
            owner_name=room["owner_name"],
            is_active=room["is_active"]
        )

        return roomOut 
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
