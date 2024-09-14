# rooms.py

# Rooms list
ROOMS = [
]

# Fetch room by id or return None if the room was not found
def get_room_by_id(room_id: int):
    for room in ROOMS:
        if room["room_id"] == room_id:
            return room
    return None