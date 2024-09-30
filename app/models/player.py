from typing import List
from uuid import UUID

from pydantic import BaseModel

from .fig_card import FigCard
from .mov_card import MovCard


class Player(BaseModel):
    player_name: str
    mov_cards: List[MovCard]
    fig_cards: List[FigCard]
    has_turn: bool

    def __init__(
        self,
        player_name: str,
        mov_cards: List[MovCard],
        fig_cards: List[FigCard],
        has_turn: bool,
    ):
        super().__init__(
            player_name=player_name,
            mov_cards=mov_cards,
            fig_cards=fig_cards,
            has_turn=has_turn,
        )
        self.validate()

    def validate(self):
        if not (0 <= len(self.mov_cards) <= 3):
            raise ValueError("mov_cards list must contain between 0 and 3 items")
        if not (0 <= len(self.fig_cards) <= 25):
            raise ValueError("fig_cards list must contain between 0 and 25 items")
