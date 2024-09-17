from game import Game

def test_game_ok():
    try:
        game = Game(game_id=1,players_names=['Yamil','Tadeo'])
        game.print_game()
    except ValueError as e:
        print(f"Error: {e}")
        assert False

def test_game_a_player():
    try:
        game = Game(game_id=1,players_names=['Yamil'])
        assert False
    except ValueError as e:
        print(f"Error: {e}")

def test_game_5_players():
    try:
        game = Game(game_id=1,players_names=['Yamil','Tadeo','Grego','Facu','Braian'])
        assert False
    except ValueError as e:
        print(f"Error: {e}")

def test_game_dup_players():
    try:
        game = Game(game_id=1,players_names=['Yamil','Yamil','Grego','Facu'])
        assert False
    except ValueError as e:
        print(f"Error: {e}")
