# FastApi
from fastapi import FastAPI, HTTPException, status
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# data, methods and classes of a room
from rooms import *

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
@app.put("/rooms/join")
def join_room_endpoint(room_id: int, player_name: str):
    try:
        room = get_room_by_id(room_id)

        if room is None:
            return {"message": "Room not found"}

        if len(room["players_names"]) == room["players_expected"]:
            return {"message": "Room is full"}
        
        if player_name in room["players_names"]:
            return {"message": "The name already exists, choose another"}
        
        room["players_names"].append(player_name)
        return {"message": f"The player {player_name} has joined the room {room_id}"}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")