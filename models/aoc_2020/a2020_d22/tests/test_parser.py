from models.common.io import InputFromString

from ..parser import parse_crab_combat_cards


def test_parse_crab_combat_cards():
    file_content = """
                   Player 1:
                   9
                   2
                   6
                   3
                   1
                   
                   Player 2:
                   5
                   8
                   4
                   7
                   10
                   """
    cards_a, cards_b = parse_crab_combat_cards(InputFromString(file_content))
    assert cards_a == [9, 2, 6, 3, 1]
    assert cards_b == [5, 8, 4, 7, 10]
