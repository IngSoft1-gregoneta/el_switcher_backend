import json
from typing import List
from pydantic import BaseModel
from .board import Board
from .fig_card import FigCard, CardColor, FigType
from .mov_card import MovCard, MovType
from .player import Player
from .room import RoomRepository
from config.repositorymanager import Session,Match
from .tile import Tile, TileColor
import random





class MatchIn(BaseModel):
    room_id: int

class MatchOut(BaseModel):
    match_id: int
    board: Board
    players: List[Player]

    def __init__(self, match_id: int):
        board = self.create_board(match_id)
        players = self.create_players(match_id)
        super().__init__(match_id=match_id, board=board, players=players)
        self.validate_match()

    def validate_room(self, match_id: int) -> List[str]:
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

    def create_board(self, match_id: int) -> Board:
        return Board(match_id)

    def create_players(self, match_id: int) -> List[Player]:
        players_names = self.validate_room(match_id)
        players = []
        index = 0
        for player_name in players_names:
            fig_cards = self.create_fig_cards(len_players=len(players_names), match_id=match_id, player_name=player_name)
            mov_cards = self.create_mov_cards(match_id=match_id, player_name=player_name)
            has_turn = index == 0
            player = Player(match_id=match_id, player_name=player_name, mov_cards=mov_cards, fig_cards=fig_cards, has_turn=has_turn)
            players.append(player)
            index = index + 1
        return players

    @staticmethod
    def create_fig_cards(len_players: int, match_id: int, player_name: str) -> List[FigCard]:
        fig_cards = []
        white_figs = list(FigType)[:7]
        for i in range(50 // len_players):
            new_fig_card = FigCard(match_id=match_id, player_name=player_name, card_color=CardColor.WHITE, fig_type=random.choice(white_figs))
            fig_cards.append(new_fig_card)
        return fig_cards

    @staticmethod
    def create_mov_cards(match_id: int, player_name: str) -> List[MovCard]:
        mov_cards = []
        for i in range(3):
            new_mov_card = MovCard(match_id=match_id, player_name=player_name, mov_type=random.choice(list(MovType)))
            mov_cards.append(new_mov_card)
        return mov_cards

MATCHS = [
]

class MatchRepository:
    def create_match(self, new_match: MatchOut):
        db = Session()
        try:
            matchdb = db.query(Match).filter(Match.match_id == new_match.match_id).one_or_none()
            if matchdb: raise ValueError("There must be exactly one room per match")
                
            players_db = []
            tiles_db = []
            for player in new_match.players:
                for card in player.mov_cards:
                    card.mov_type = card.mov_type.value
                for card in player.fig_cards:
                    card.card_color = card.card_color.value
                    card.fig_type = card.fig_type.value
                player.mov_cards = [Movcard.model_dump() for Movcard in player.mov_cards]
                player.fig_cards = [figcard.model_dump() for figcard in player.fig_cards]
                player = player.model_dump()
                players_db.append(player)
            for tile in new_match.board.tiles:
                tile.tile_color = tile.tile_color.value
                tiles_db.append(tile.model_dump())
            board_db = (tiles_db, new_match.match_id)
                
            matchdb = Match(
                match_id = new_match.match_id,
                room_id = new_match.match_id,
                board = board_db,
                players = players_db
                )
            db.add(matchdb)
            db.commit()
        finally:
            db.close()
            
    def get_match_by_id(self, match_id_selected: int) -> MatchOut:
        db = Session()
        try:
            matchdb = db.query(Match).filter(Match.match_id == match_id_selected).one_or_none()
            if not matchdb:
                return None

            # Deserializar el tablero
            board_data = matchdb.board
            tiles_db = board_data[0]
            tileslist = []
            for tile in tiles_db:
                tileslist.append(Tile.model_construct(
                    tile_color=TileColor(tile["tile_color"]).value,  
                    tile_pos_x=tile["tile_pos_x"], 
                    tile_pos_y=tile["tile_pos_y"]
                ))

            board_db = Board.model_construct(match_id = board_data[1], tiles = tileslist)
        
            # Deserializar jugadores
            players_db = []
            players_data = matchdb.players
            for player_data in players_data:    
                player_data_id = player_data["match_id"]
                player_data_name = player_data["player_name"]
                player_data_mov_cards = player_data["mov_cards"]
                player_data_fig_cards = player_data["fig_cards"]
                player_data_has_turn = player_data["has_turn"]
                fig_cards_db = []
                for fig_card in player_data_fig_cards:
                    fig_cards_db.append(FigCard.model_construct(match_id = fig_card["match_id"],player_name= fig_card["player_name"],card_color= CardColor(fig_card["card_color"]).value,fig_type = FigType(fig_card["fig_type"]).value,is_visible = fig_card["is_visible"]))
                mov_cards_db = []
                for mov_card in player_data_mov_cards:
                    mov_cards_db.append(MovCard.model_construct(match_id=mov_card["match_id"],player_name = mov_card["player_name"],mov_type = MovType(mov_card["mov_type"]).value))
                players_db.append(Player.model_construct(match_id= player_data_id,player_name= player_data_name,mov_cards =mov_cards_db,fig_cards = fig_cards_db,has_turn =player_data_has_turn))
            # Devolver la instancia de MatchOut
            match = MatchOut.model_construct(match_id = match_id_selected, board=board_db, players = players_db)
            return match
        finally:
            db.close()
            
    def delete(self,id):
        db = Session()
        try:
            todelete = db.query(Match).filter(Match.match_id == id).one_or_none()
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
