from .match import *
from match_handler import *
from state_handler import *

match_repository = MatchRepository()

class VisiblePlayer(BaseModel):
    player_name: str
    visible_fig_cards: List[FigCard]
    visible_mov_cards: List[MovCard]
    deck_len: int 
    has_turn: bool

    def __init__(self, match_id: UUID, player_name: str):
        visible_fig_cards = self.get_visible_fig_cards(match_id, player_name)
        visible_mov_cards = self.get_visible_mov_cards(match_id, player_name)
        deck_len = self.get_deck_len(match_id, player_name)
        has_turn = self.get_has_turn(match_id, player_name)
        super().__init__(player_name=player_name,
                         visible_fig_cards=visible_fig_cards,
                         visible_mov_cards=visible_mov_cards,
                         deck_len=deck_len,
                         has_turn=has_turn)
 
    def get_visible_fig_cards(self, match_id, player_name) -> List[FigCard]:
        try:
            match = get_parcial_match(match_id)
            player = match.get_player_by_name(player_name)
            visible_fig_cards = []
            for fig_card in player.fig_cards:
                if fig_card.is_visible is True:
                    visible_fig_cards.append(fig_card)
            return visible_fig_cards
        except Exception as e:
            raise e
    
    def get_visible_mov_cards(self, match_id: UUID, player_name: str) -> List[MovCard]:
        try:
            match = get_parcial_match(match_id)
            player = match.get_player_by_name(player_name)
            mov_cards = []
            for card in player.mov_cards:
                if card.is_used:
                    mov_cards.append(card)  
            return mov_cards 
        except Exception as e:
            raise e 

    def get_deck_len(self, match_id, player_name) -> int:
        try:
            match = get_parcial_match(match_id)
            player = match.get_player_by_name(player_name)
            return len(player.fig_cards)
        except Exception as e:
            raise e
        
    def get_has_turn(self, match_id, player_name) -> bool:
        try:
            match = get_parcial_match(match_id)
            player = match.get_player_by_name(player_name)
            return player.has_turn
        except Exception as e:
            raise e

class Me(BaseModel):
    player_name: str
    visible_fig_cards: List[FigCard]
    mov_cards: List[MovCard]
    deck_len: int 
    has_turn: bool

    def __init__(self, match_id: UUID, player_name: str):
        visible_fig_cards = self.get_visible_fig_cards(match_id, player_name)
        mov_cards = self.get_player_me_mov_cards(match_id, player_name)
        deck_len = self.get_deck_len(match_id, player_name)
        has_turn = self.get_has_turn(match_id, player_name)

        super().__init__(player_name=player_name,
                         visible_fig_cards=visible_fig_cards,
                         mov_cards=mov_cards,
                         deck_len=deck_len,
                         has_turn=has_turn)
    
    def get_player_me_mov_cards(self, match_id: UUID, player_name: str) -> List[MovCard]:
        try:
            match = get_parcial_match(match_id)
            player = match.get_player_by_name(player_name)

            return player.mov_cards 
        except Exception as e:
            raise e 

    def get_visible_fig_cards(self, match_id, player_name) -> List[FigCard]:
        try:
            match = get_parcial_match(match_id)
            player = match.get_player_by_name(player_name)
            visible_fig_cards = []
            for fig_card in player.fig_cards:
                if fig_card.is_visible is True:
                    visible_fig_cards.append(fig_card)
            return visible_fig_cards
        except Exception as e:
            raise e
        
    def get_deck_len(self, match_id, player_name) -> int:
        try:
            match = get_parcial_match(match_id)
            player = match.get_player_by_name(player_name)
            return len(player.fig_cards)
        except Exception as e:
            raise e
        
    def get_has_turn(self, match_id, player_name) -> bool:
        try:
            match = get_parcial_match(match_id)
            player = match.get_player_by_name(player_name)
            return player.has_turn
        except Exception as e:
            raise e

class VisibleMatchData(BaseModel):
    match_id: str
    me: Me
    other_players: List[VisiblePlayer]
    visible_mov_cards: List[MovCard]
    state_number: int
    board: Board
    winner: Union[Player, None]

    def __init__(self, match_id: UUID, player_name: str):
        self.validate_player(match_id, player_name)
        match = get_parcial_match(match_id)
        me = Me(match_id=match_id, player_name=player_name)
        other_players = self.get_other_players(match_id, player_name)
        winner = self.get_winner(match_id=match_id)
        visible_mov_cards = self.get_visible_mov_cards(match_id)
        state_number = self.get_state_number(match_id)
        board = match.board
        super().__init__(match_id=str(match_id),
                        me=me,
                        other_players=other_players,
                        visible_mov_cards=visible_mov_cards,
                        state_number=state_number,
                        board=board,
                        winner=winner)
        
   
    def get_other_players(self, match_id, player_name) -> List[VisiblePlayer]:
        try:
            match = get_parcial_match(match_id)
            other_players = []
            for player in match.players:
                if player.player_name != player_name:
                    other_player = VisiblePlayer(match_id=match_id, player_name=player.player_name)
                    other_players.append(other_player)
            return other_players
        except Exception as e:
            raise e

    def get_visible_mov_cards(self, match_id) -> List[MovCard]:
        try:
            visible_mov_cards = []
            match = get_parcial_match(match_id)
            for player in match.players:
                if player.has_turn is True:
                    for mov_card in player.mov_cards:
                        if mov_card.is_used:
                            visible_mov_cards.append(mov_card)
            return visible_mov_cards

        except Exception as e:
            raise e
        
    def get_state_number(self, match_id) -> int:
        try:
            match = get_parcial_match(match_id)
            state_number = match.state
            return state_number
        except Exception as e:
            raise e
            
    def validate_player(self, match_id, player_name):
        match = get_parcial_match(match_id)
        if match is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Match not found")
        player = match.get_player_by_name(player_name)
        if player is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Player {player_name} not found")
        
    def get_winner(self, match_id):
        try:
            winner = None
            match = get_parcial_match(match_id=match_id)
            if len(match.players) == 1:
                winner = match.players[0]
            for player in match.players:
                if len(player.mov_cards) == 0:
                    winner = player
            return winner
        except Exception as e:
            raise e


