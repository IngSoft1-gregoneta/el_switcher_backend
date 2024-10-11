from models.mov_card import MovCard, MovType, MovStatus
from models.mov_card import MovCard, MovType, MovStatus
import random

def test_random_mov_card():
    try:
        card = MovCard()
        assert card.mov_type in list(MovType), f"{card.mov_type} is not a valid mov card"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_valid_mov_card():
    mov_type = random.choice(list(MovType))
    try:
        card = MovCard(mov_type=mov_type)
        assert card.mov_type == mov_type, f"mov type {card.mov_type} must be {mov_type}"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_valid_mov_card_str():
    mov_type = "mov1"
    try:
        card = MovCard(mov_type=mov_type)
        assert card.mov_type == MovType.mov1, f"mov type {card.mov_type} must be {mov_type}"
    except ValueError as e:
        assert False, f"Error: {e}"
    
def test_invalid_mov_card_str():
    mov_type = "Diagonal"
    try:
        card = MovCard(mov_type=mov_type)
        assert False, f"{card.mov_type} is not a mov type"
    except ValueError as e:
        assert True

def test_use_mov_card():
    try:
        mov_card = MovCard(mov_type=MovType.mov1,mov_status=MovStatus.PLAYED)
        mov_card.use_mov_card()
        assert mov_card.is_used == True, "mov_card should be marked as used"
        assert mov_card.mov_status == MovStatus.PLAYED, f"mov status should be {MovStatus.PLAYED}, but got {mov_card.mov_status}"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_confirm_mov_card():
    try:
        mov_card = MovCard(mov_type=MovType.mov1)
        mov_card.use_mov_card()
        mov_card.confirm_mov_card()
        assert mov_card.is_used == True, "mov_card should be marked as used"
        assert mov_card.mov_status == MovStatus.CONFIRMED, f"mov status should be {MovStatus.CONFIRMED}, but got {mov_card.mov_status}"
    except ValueError as e:
        assert False, f"Error: {e}"


def test_held_mov_card():
    try:
        mov_card = MovCard(mov_type=MovType.mov1, mov_status=MovStatus.HELD)
        mov_card.held_mov_card()
        assert mov_card.is_used == False, "mov_card should be marked as not used"
        assert mov_card.mov_status == MovStatus.HELD, f"mov status should be {MovStatus.HELD}, but got {mov_card.mov_status}"
    except ValueError as e:
        assert False, f"Error: {e}"
        
def test_coords_mov_card():
    mov_card = MovCard(mov_type=MovType.mov1, mov_status=MovStatus.HELD)
    assert(mov_card.vectors == [(-2,-2),(2,-2),(-2,2),(2,2)])
    mov_card = MovCard(mov_type=MovType.mov2, mov_status=MovStatus.HELD)
    assert(mov_card.vectors == [(-2,0),(0,-2),(2,0),(0,2)])
    mov_card = MovCard(mov_type=MovType.mov3, mov_status=MovStatus.HELD)
    assert(mov_card.vectors == [(-1,0),(0,-1),(1,0),(0,1)])
    mov_card = MovCard(mov_type=MovType.mov4, mov_status=MovStatus.HELD)
    assert(mov_card.vectors == [(-1,-1),(1,-1),(-1,1),(1,1)])
    mov_card = MovCard(mov_type=MovType.mov5, mov_status=MovStatus.HELD)
    assert(mov_card.vectors == [(-2,-1),(1,-2),(2,1),(-1,2)])
    mov_card = MovCard(mov_type=MovType.mov6, mov_status=MovStatus.HELD)
    assert(mov_card.vectors == [(-2,1),(-1,-2),(2,-1),(1,2)])
    mov_card = MovCard(mov_type=MovType.mov7, mov_status=MovStatus.HELD)
    assert(mov_card.vectors == [(-4,0),(0,-4),(4,0),(0,4)])