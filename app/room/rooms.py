# rooms.py
import random
# Rooms list
ROOMS = [
]

# Fetch room by id or return None if the room was not found
def get_room_by_id(room_id: int):
    for room in ROOMS:
        if room["room_id"] == room_id:
            return room
    return None

def sort_players(room):
        if room["creator"] in room["players"]:
            #Chequeamos que los jugadores sean mas de 2, porque sino estamos haciendo trabajo innecesario
            if room["players_expected"] <= 2:  
                 room["players"].remove(room["creator"])
                 room["players"].insert(0,room["creator"])
            else:
                room["players"].remove(room["creator"])
                random.shuffle(room["players"])
                room["players"].insert(0,room["creator"])