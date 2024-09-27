from typing import Any, Union
from uuid import UUID

from fastapi import HTTPException, status

from manager.manager import ConnectionManager

#from manager.manager import ConnectionManager
from models.room import RoomIn, RoomOut, RoomRepository
    
manager = ConnectionManager()

class RoomHandler:
    
    def __init__(self):
        self.repo = RoomRepository()
    
    async def get_all_rooms(self):
     try:
         return self.repo.get_rooms()
     except Exception:
         raise("Error getting rooms")
     
     
    async def get_data_from_a_room(self,room_id: int) -> Union[RoomOut, dict]:
     try:
         room = self.repo.get_room_by_id(room_id)
         if room is None:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
         return room
     except Exception:
         raise("Error getting room")
    
    
    async def create_bind_and_broadcast(self, room_id: UUID, user_id: UUID): 
        try:
             manager.bind_room(room_id, user_id)
             await manager.broadcast_not_playing("LISTA")
        except Exception as e:
            raise Exception(f"Error:{str(e)}")
      
    
    async def create_room_modularized(self, new_room: RoomIn) -> RoomOut:
        if new_room.players_expected < 2 or new_room.players_expected > 4:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail="Wrong amount of players"
         )
         
        existing_room = self.repo.check_for_names(new_room.room_name)
        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room name already exists"
                )
         
        return self.repo.create_room(new_room)
    
    
    async def join_bind_and_broadcast(self, room_id: UUID, user_id: UUID):
        try:
            # TODO:  ENUMS PARA MANAGER, o mejor encargarse todo el la clase
            manager.bind_room(room_id, user_id)
            await manager.broadcast_not_playing("LISTA")
            await manager.broadcast_by_room(room_id, "ROOM")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
        
    
    async def join_room_modularized(self, room_id: int, player_name: str, user_id: UUID):
        try:
            room = self.repo.get_room_by_id(room_id)
            if room is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            if len(room.players_names) == room.players_expected:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Room is full"
                    )
                
            if player_name in room.players_names:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Player name is already on the room, choose another name",
                    )
            
            self.repo.update_players(room.players_names, player_name, room_id, "add")
            return self.repo.get_room_by_id(room_id)
        
        except HTTPException as http_exc:
        # si es una HTTPException, dejamos que pase como está 
         raise http_exc
     
    async def leave_unbind_and_broadcast(self, room_id: UUID, user_id: UUID):
        try:
            # TODO:  ENUMS PARA MANAGER, o mejor encargarse todo el la clase
            manager.unbind_room(room_id, user_id)
            await manager.broadcast_not_playing("LISTA")
            await manager.broadcast_by_room(room_id, "ROOM")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
        
    
    async def leave_room_modularized(self, room_id: int, player_name: str, user_id: UUID):
        try:
            room = self.repo.get_room_by_id(room_id)
            if room is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            if not (player_name in room.players_names):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            if player_name == room.owner_name: # si el owner abandona la sala, eliminar la sala
                self.repo.delete(room_id)
                return {"message": f"The owner {player_name} has left. Room {room_id} has been deleted."}
      
            
            self.repo.update_players(room.players_names, player_name, room_id, "remove")
            return self.repo.get_room_by_id(room_id)
        
        except HTTPException as http_exc:
        # si es una HTTPException, dejamos que pase como está 
         raise http_exc
 
 


        
        