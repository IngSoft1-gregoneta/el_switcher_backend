# Module dedicated to storing models

# List that stores rooms
ROOMS = []

def get_room_by_id(room_id: int):
    for room in ROOMS:
        if room["room_id"] == room_id:
            return room
    return None