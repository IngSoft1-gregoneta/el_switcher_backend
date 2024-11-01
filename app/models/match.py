import json
from typing import List
from enum import Enum
from pydantic import BaseModel
from .board import *
from .fig_card import FigCard, CardColor, FigType
from .mov_card import MovCard, MovType
from .player import Player
from .room import *
from config.repositorymanager import Session,Match
from models.tile import Tile, TileColor
import random
from fastapi import HTTPException, status
from typing import Tuple
import copy 

class MatchOut(BaseModel):
    match_id: UUID
    state: int
    board: Board
    players: List[Player]

    def __init__(self, match_id: UUID):
        board = self.create_board()
        players = self.create_players(match_id)
        super().__init__(match_id=match_id, board=board, players=players, state=0)
        self.validate_match()

    def validate_room(self, match_id: UUID) -> List[str]:
        repo = RoomRepository()
        rooms_whit_match_id = 0
        for room in repo.get_rooms():
            if room["room_id"] == match_id:
                 room_of_match = room
                 rooms_whit_match_id = rooms_whit_match_id + 1
        if rooms_whit_match_id != 1:
            raise ValueError("There must be exactly one room per match")  
        if not len(room_of_match["players_names"]) in range(2, 5):
            raise ValueError("There are not between 2 and 4 players") 
        if room_of_match["players_expected"] != len(room_of_match["players_names"]):
            raise ValueError("There must be exactly players expected amount of players")  
        return room_of_match["players_names"]
 
    def validate_match(self):
        turns_count = sum(player.has_turn for player in self.players)
        if turns_count != 1:
            raise ValueError("There must be exactly one player with the turn")

    def create_board(self) -> Board:
        return Board()

    def create_players(self, match_id: UUID) -> List[Player]:
        players_names = self.validate_room(match_id)
        players = []
        
        white_deck = list(FigType)[1:8] * 2  # 14 cartas blancas, dos de cada figura
        blue_deck = list(FigType)[8:] * 2  # 36 cartas azules, dos de cada figura
        random.shuffle(white_deck)
        random.shuffle(blue_deck)
        
        white_per_player = 14 // len(players_names)
        blue_per_player = 36 // len(players_names)

        index = 0
        for player_name in players_names:
            fig_cards, white_deck, blue_deck = self.create_fig_cards(white_per_player,blue_per_player,white_deck,blue_deck)
            for i in range(3): fig_cards[i].is_visible = True
            mov_cards = self.create_mov_cards()
            has_turn = index == 0
            player = Player(player_name=player_name, mov_cards=mov_cards, fig_cards=fig_cards, has_turn=has_turn)
            players.append(player)
            index = index + 1
        return players


    @staticmethod
    def create_fig_cards(white_per_player: int, 
                         blue_per_player: int, white_deck: List[FigType],
                        blue_deck: List[FigType]) -> Tuple[List[FigCard], List[FigType], List[FigType]]:
        fig_cards = []
        for i in range(white_per_player):
            fig_type = white_deck.pop(0)
            new_fig_card = FigCard(
                card_color=CardColor.WHITE,
                fig_type=fig_type,
                is_visible=False,
                is_blocked=False
            )
            fig_cards.append(new_fig_card)
        for i in range(blue_per_player):
            fig_type = blue_deck.pop(0)
            new_fig_card = FigCard(
                card_color=CardColor.BLUE,
                fig_type=fig_type,
                is_visible=False,
                is_blocked=False
            )
            fig_cards.append(new_fig_card)
            random.shuffle(fig_cards)
        return fig_cards, white_deck, blue_deck

    @staticmethod
    def create_mov_cards() -> List[MovCard]:
        mov_cards = []
        for i in range(3):
            new_mov_card = MovCard(
            mov_type=random.choice(list(MovType)),
            is_used=False
        )
            mov_cards.append(new_mov_card)
        return mov_cards

    def get_player_by_name(self, player_name) -> Player | None:
        for player in self.players:
            if player.player_name == player_name:
                return player
        return None

class MatchRepository:
    def create_match(self, new_match: MatchOut):
        db = Session()
        try:
            matchdb = db.query(Match).filter(Match.match_id == str(new_match.match_id)).one_or_none()
            if matchdb: raise ValueError("There must be exactly one room per match")
            players_db = []
            tiles_db = []
            for player in new_match.players:
                for card in player.mov_cards:
                    card.mov_type = card.mov_type.value
                    card.is_used = card.is_used
                for card in player.fig_cards:
                    card.card_color = card.card_color.value
                    card.fig_type = card.fig_type.value
                player.mov_cards = [Movcard.model_dump() for Movcard in player.mov_cards]
                player.fig_cards = [figcard.model_dump() for figcard in player.fig_cards]
                player = player.model_dump()
                players_db.append(player)
            for tile in new_match.board.tiles:
                tile.tile_color = tile.tile_color.value
                tile.tile_in_figure = tile.tile_in_figure.value
                tiles_db.append(tile.model_dump())
            board_db = (tiles_db)
            matchdb = Match(
                match_id = str(new_match.match_id),
                board = board_db,
                players = players_db,
                )
            db.add(matchdb)
            db.commit()

        finally:
            db.close()
            
    def get_match_by_id(self, match_id_selected: UUID) -> MatchOut:
        db = Session()
        try:
            matchdb = db.query(Match).filter(Match.match_id == str(match_id_selected)).one_or_none()
            if not matchdb:
                return None
            # Deserializar el tablero
            board_data = matchdb.board
            tiles_db = board_data
            tileslist = []
            for tile in tiles_db:
                tileslist.append(Tile.model_construct(
                    tile_color=TileColor(tile["tile_color"]).value, 
                    tile_in_figure=FigType(tile["tile_in_figure"]).value, 
                    tile_pos_x=tile["tile_pos_x"], 
                    tile_pos_y=tile["tile_pos_y"]
                )) 

            board_db = Board.model_construct(tiles = tileslist)

            # Deserializar jugadores
            players_db = []
            players_data = matchdb.players
            for player_data in players_data:    
                player_data_name = player_data["player_name"]
                player_data_mov_cards = player_data["mov_cards"]
                player_data_fig_cards = player_data["fig_cards"]
                player_data_has_turn = player_data["has_turn"]

                fig_cards_db = []
                for fig_card in player_data_fig_cards:
                    fig_cards_db.append(FigCard.model_construct(
                        card_color= CardColor(fig_card["card_color"]).value,
                        fig_type = FigType(fig_card["fig_type"]).value,
                        is_visible = fig_card["is_visible"],
                        is_blocked = fig_card["is_blocked"]
                        )
                    )
                mov_cards_db = []
                for mov_card in player_data_mov_cards:
                    card = MovCard(
                        mov_type = MovType(mov_card["mov_type"]),
                        is_used=mov_card["is_used"])
                    card.mov_type = card.mov_type.value
                    mov_cards_db.append(card)
                players_db.append(Player.model_construct(player_name= player_data_name,mov_cards =mov_cards_db,fig_cards = fig_cards_db,has_turn =player_data_has_turn))
            # Devolver la instancia de MatchOut
            match = MatchOut.model_construct(match_id = str(match_id_selected), state = 0, board=board_db, players = players_db)
            return match
        finally:
            db.close()
            
    def delete(self,id):
        db = Session()
        try:
            todelete = db.query(Match).filter(Match.match_id == str(id)).one_or_none()
            db.delete(todelete)
            db.commit()
        finally:
            db.close()
            
    def delete_matchs(self):
     db = Session()
     try:
         db.query(Match).delete()
         db.commit()
     finally:
         db.close()


    def delete_player(self, match_id: UUID, player_name: str):
        match = self.get_match_by_id(match_id)
        if match is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
        player_to_remove = None
        for player in match.players:
            if player.player_name == player_name:
                player_to_remove = player
        if player_to_remove == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
        # Pasa el turno antes de borrar
        if player_to_remove.has_turn:
            self.end_turn(match=match, player_name=player_to_remove.player_name)
        match.players.remove(player_to_remove)
        if len(match.players) == 0:
            self.delete(match_id)
            return "Match destroyed"
        self.update_match(match)
        return match

    def end_turn(self, match: MatchOut, player_name: str):
        for i in range(len(match.players)):
            if match.players[i].player_name == player_name:
                match.players[i].hand_mov_cards()
                has_cards_blocked = False
                for fig_card in match.players[i].fig_cards:
                    if fig_card.is_blocked:
                        has_cards_blocked = True
                if not has_cards_blocked:
                    match.players[i].hand_fig_cards()
                match.players[i].has_turn = False # this player
                match.players[(i+1)%len(match.players)].has_turn = True # next player
                match.state = 0
        self.update_match(match)

    def update_match(self, match_: MatchOut):
            match = copy.deepcopy(match_)
            db = Session()
            try:
                matchdb = db.query(Match).filter(Match.match_id == str(match.match_id)).one_or_none()

                players_db = []
                tiles_db = []
                for tile in match.board.tiles:
                    tiles_db.append(tile.model_dump())
                board_db = (tiles_db)
                for player in match.players:
                    player = player.model_dump()
                    players_db.append(player)

                matchdb = Match(
                    match_id = str(match.match_id),
                    board = board_db,
                    players = players_db,
                    )
                self.delete(match.match_id)
                db.add(matchdb)
                db.commit()
            except Exception as e:
                db.rollback()
                raise
            finally:
                db.close()
