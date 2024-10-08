from uuid import UUID
from fastapi import HTTPException,status
from config.repositorymanager import Session
from config.Tables_initializer import Match
from models.match import MatchOut
from models.mov_card import MovCard,MovType
from models.fig_card import FigCard,FigType,CardColor
from models.board import Board
from models.tile import Tile,TileColor
from models.player import Player




class MatchRepository:
    def serialize(self,match: MatchOut):
            players_db = []
            tiles_db = []
            for player in match.players:
                for card in player.mov_cards:
                    card.mov_type = card.mov_type
                for card in player.fig_cards:
                    card.card_color = card.card_color
                    card.fig_type = card.fig_type
                player.mov_cards = [Movcard.model_dump() for Movcard in player.mov_cards]
                player.fig_cards = [figcard.model_dump() for figcard in player.fig_cards]
                player = player.model_dump()
                players_db.append(player)
            for tile in match.board.tiles:
                tile.tile_color = tile.tile_color
                tiles_db.append(tile.model_dump())
            board_db = (tiles_db)
            matchdb = Match(
                match_id = str(match.match_id),
                board = board_db,
                players = players_db
                )
            return matchdb
        
    def deserialize(self,matchdb: Match):
            board_data = matchdb.board
            tiles_db = board_data
            tileslist = []
            for tile in tiles_db:
                tileslist.append(Tile.model_construct(
                    tile_color=TileColor(tile["tile_color"]).value,  
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
                        is_visible = fig_card["is_visible"]))
                mov_cards_db = []
                for mov_card in player_data_mov_cards:
                    mov_cards_db.append(MovCard.model_construct(
                        mov_type = MovType(mov_card["mov_type"]).value))
                players_db.append(Player.model_construct(player_name= player_data_name,mov_cards =mov_cards_db,fig_cards = fig_cards_db,has_turn =player_data_has_turn))
            # Devolver la instancia de MatchOut
            match = MatchOut.model_construct(match_id = str(matchdb.match_id), board=board_db, players = players_db)
            return match
    
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
            board_db = (tiles_db)
            matchdb = Match(
                match_id = str(new_match.match_id),
                board = board_db,
                players = players_db
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
            match = self.deserialize(matchdb)
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


    def delete_player(self, player_name: str, match_id: UUID):
        db = Session()
        try:
            match = self.get_match_by_id(match_id)
            if match is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="match not found")
            matchdb = db.query(Match).filter(Match.match_id == str(match_id)).one_or_none()
            player_to_remove = None
            for player in match.players:
                if player.player_name == player_name:
                    player_to_remove = player
            if player_to_remove == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
            match.players.remove(player_to_remove)
            if len(match.players) == 0:
                self.delete(match_id)
                return "Match destroyed"
            matchdb = self.serialize(match)
            self.delete(match_id)
            db.add(matchdb)
            db.commit()

            return match
        finally:
            db.close()

    def end_turn(self, match_id: UUID, player_name: str):
        db = Session()
        try:
            match = self.get_match_by_id(match_id)
            if match is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
            target_player = match.get_player_by_name(player_name)
            if target_player is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
            if target_player.has_turn is False:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player has not the turn")
            for i in range(len(match.players)):
                if match.players[i].player_name == player_name:
                    match.players[i].has_turn = False # this player
                    match.players[(i+1)%len(match.players)].has_turn = True # next player
            matchdb = db.query(Match).filter(Match.match_id == str(match_id)).one_or_none()
            matchdb = self.serialize(match)
            self.delete(match_id)
            db.add(matchdb)
            db.commit()
            return match
        finally:
            db.close()