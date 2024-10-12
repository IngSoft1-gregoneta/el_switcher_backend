from typing import Any, Union, Dict, List
from uuid import UUID
import copy
from fastapi import HTTPException, status
from models.match import MatchOut, MatchRepository
from models.room import RoomRepository
from models.visible_match import *
import figure_detector
import state_handler
import switcher

class MatchHandler:
    def __init__(self):
        self.repo = MatchRepository()

    async def create_match(self, match_id: UUID, owner_name: str):
        repo_room = RoomRepository()
        try:
            room = repo_room.get_room_by_id(match_id)
            if room is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
                )
            if room.owner_name != owner_name:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only the owner can create a match",
                )
            match = MatchOut(match_id)
            self.repo.create_match(match)
            match = self.repo.get_match_by_id(match.match_id)
            fig_types = self.get_valid_fig_types(match)
            match.board = figure_detector.figures_detector(match.board, fig_types)
            state_handler.add_parcial_match(match)
            self.repo.update_match(match)
            return match.model_dump(mode="json")

        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bad request: {str(ve)}",
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    
    def get_valid_fig_types(self, match: MatchOut) -> List[str]:
        fig_types: List[str] = []    
        for player in match.players:
            for i in range(len(player.fig_cards)):
                if player.fig_cards[i].is_visible:
                    fig_types.append(player.fig_cards[i].fig_type)
        return fig_types

    async def get_match_by_id(self, match_id: UUID) -> Union[MatchOut, dict]:
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

    async def leave_match(
        self, player_name: str, match_id: UUID
    ) -> Union[MatchOut, str]:
        try:
            match = self.repo.delete_player(player_name, match_id)
            return match
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    async def get_visible_data_by_player(
        self, match_id: UUID, player_name: str
    ) -> VisibleMatchData:
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

    async def end_turn(self, match_id: UUID, player_name: str):
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
    
    async def do_parcial_mov(self, match_id: UUID, player_name: str, card_index: int, x1: int, y1: int, x2: int, y2:int):
        match = state_handler.get_parcial_match(match_id)
        if match is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")   
        new_match = copy.deepcopy(match)
        player = new_match.get_player_by_name(player_name)
        if player is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")   
        if not player.has_turn:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player has not turn")   
        if card_index < 0 or card_index >= len(player.mov_cards):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")   
        mov_card = player.mov_cards[card_index]
        if switcher.is_valid_movement(mov_card.mov_type, x1, y1, x2, y2):
            switcher.switch(new_match.board, mov_card.mov_type, x1, y1, x2, y2)
            fig_types = self.get_valid_fig_types(new_match)
            new_match.board = figure_detector.figures_detector(new_match.board, fig_types)
            mov_card.use_mov_card()
            state_handler.add_parcial_match(new_match)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid movement")   
         
    async def check_winner(self, match_id: UUID):
        try:
            match = self.repo.get_match_by_id(match_id)
            if match is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
            
            winner = None
            # Caso 1: jugador sin cartas de figura
            # Caso 2: ultimo jugador en partida
            for player in match.players:
                # No tiene mas cartas de figura
                if len(player.fig_cards) == 0:
                    winner = player.player_name

            if len(match.players) == 1:
                winner = match.players[0].player_name

            # Si !caso1 & !caso2 => winner is None
            return winner
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    