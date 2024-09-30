from typing import Any, Union
from uuid import UUID

from fastapi import HTTPException, status

from models.match import MatchIn, MatchOut, MatchRepository
from models.room import RoomRepository
from models.visible_match import *

class MatchHandler:
    def __init__(self):
        self.repo = MatchRepository()
        
    async def create_match(self, match_in: MatchIn, owner_name: str):
        repo_room = RoomRepository()
        room = repo_room.get_room_by_id(match_in.room_id)  # Asegúrate de tener este método en tu repositorio
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Bad request: There must be exactly one room per match')
        
        if room.owner_name != owner_name:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the owner can create a match")
        
        try:
            match = MatchOut(match_in.room_id)
            self.repo.create_match(match)
            return self.repo.get_match_by_id(match.match_id).model_dump(mode="json")
        except ValueError as ve:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: {str(ve)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")
        
        
    async def get_match_by_id(self, match_id: int) -> Union[MatchOut, dict]:
        try:
            match = self.repo.get_match_by_id(match_id)
            if match is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return match
        
        except Exception as e:
            if isinstance(e, HTTPException):
               raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
        
    
    async def leave_match(self, player_name: str, match_id: int) -> Union[MatchOut, str]:
        try:
            match = self.repo.delete_player(player_name,match_id)
            return match
        
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
        
    async def get_visible_data_by_player(self, match_id: int, player_name: str) -> VisibleMatchData:
        try:
            visible_match = VisibleMatchData(match_id=match_id, player_name=player_name)
            return visible_match
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    
    async def end_turn(self, match_id: int, player_name: str) -> MatchOut:
        try:
            match = self.repo.end_turn(match_id=match_id, player_name=player_name)
            return match
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )