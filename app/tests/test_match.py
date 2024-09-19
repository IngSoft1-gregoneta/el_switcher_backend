from match import Match

def test_match_2_players():
    has_turn_count = 0
    try:
        match = Match(match_id=1,players_names=['Yamil','Tadeo'])
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 25, f"expected 50 fig cards between 2 players (25), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_match_3_players():
    has_turn_count = 0
    try:
        match = Match(match_id=1,players_names=['Yamil','Tadeo', 'Braian'])
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 16, f"expected 50 fig cards between 3 players (16), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_match_4_players():
    has_turn_count = 0
    try:
        match = Match(match_id=1,players_names=['Yamil','Tadeo', 'Braian', 'Facu'])
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 12, f"expected 50 fig cards between 4 players (12), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_match_a_player():
    try:
        match = Match(match_id=1,players_names=['Yamil'])
        assert False
    except ValueError as e:
        assert True

def test_match_5_players():
    try:
        match = Match(match_id=1,players_names=['Yamil','Tadeo','Grego','Facu','Braian'])
        assert False
    except ValueError as e:
        assert True


def test_match_dup_players():
    try:
        match = Match(match_id=1,players_names=['Yamil','Yamil','Grego','Facu'])
        assert False
    except ValueError as e:
        assert True

