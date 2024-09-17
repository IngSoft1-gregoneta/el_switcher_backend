from game import Game

def test_game():
    try:
        game = Game(game_id=1,players_names=['Yamil','Tadeo','Grego','Braian'])
        game.print_game()
    except ValueError as e:
        print(f"Error: {e}")
        assert False