from config.Tables_initializer import Match, Playerdb
from config.repositorymanager import Session
from sqlalchemy.exc import SQLAlchemyError
from models.player import Player
from models.fig_card import FigCard, FigType,CardColor
from models.mov_card import MovCard, MovType


class PlayerRepository:
    @staticmethod
    def serialize(fig_cards: list[FigCard], mov_cards: list[MovCard]):
        fig_cardsdb = []
        mov_cardsdb = []
        for card in fig_cards:
            card.card_color = card.card_color.value
            card.fig_type = card.fig_type.value
            fig_cardsdb.append(card.model_dump())
        for card in mov_cards:
            card.mov_type = card.mov_type.value
            mov_cardsdb.append(card.model_dump())
        return fig_cardsdb, mov_cardsdb
    @staticmethod
    def deserialize(fig_cards_data, mov_cards_data):
        fig_cards = []
        mov_cards = []
        
        # Deserializar FigCards
        for card_data in fig_cards_data:
            card = FigCard.model_construct(
                card_color=CardColor(card_data['card_color']).value,
                fig_type=FigType(card_data['fig_type']).value,
            )
            fig_cards.append(card)
        
        # Deserializar MovCards
        for card_data in mov_cards_data:
            card = MovCard.model_construct(
                mov_type=MovType(mov_type = card_data['mov_type']).value)
            mov_cards.append(card)
        
        return fig_cards, mov_cards
    def create_player(self,Player:Player,id: int, match: Match):
        db = Session()
        try:
            fig_cardsdb,mov_cardsdb = self.serialize(Player.fig_cards,Player.mov_cards)
            playerdb = Playerdb(
                Matchid = id,
                player_id = Player.player_id,
                player_name = Player.player_name,
                fig_cards = fig_cardsdb,
                mov_cards = mov_cardsdb,
                has_turn = Player.has_turn,
                match = match
            )
            db.add(playerdb)
            db.commit()
            return playerdb
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Error during create_player")
        finally:
            db.close()
    def get_player_by_name(self,match_id: int, player_name:str):
        db = Session()
        try:
            playerdb = db.query(Playerdb).filter_by(player_name=player_name, Matchid=match_id).first()
            
            if playerdb is None:
                raise ValueError("NOT FOUND(player_repo, get_player_by_name)")
            
            fig_cards,mov_cards = self.deserialize(playerdb[fig_cards],playerdb[mov_cards])
            
            player = Player.model_construct(
                player_name = playerdb["player_name"],
                fig_cards = fig_cards,
                mov_cards = mov_cards,
                has_turn = playerdb["has_turn"]
            )
            return player
        finally:
            db.close()