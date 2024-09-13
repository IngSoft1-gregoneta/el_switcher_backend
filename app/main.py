# FastApi
from fastapi import FastAPI, HTTPException, status
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# data, methods and classes of a room
from room import rooms
from typing import Optional

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# endpoint for room join request 
@app.put("/rooms/join/")
def join_room_endpoint(room_id: int, player_name: str):
    try:
        room = rooms.get_room_by_id(room_id)

        if room == None:
            return {"message": "Room not found"}

        if len(room["players"]) == room["players_expected"]:
            return {"message": "Room is full"}
        
        room["players"].append(player_name)
        return {"message": f"The player {player_name} has joined the room {room_id}"}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

