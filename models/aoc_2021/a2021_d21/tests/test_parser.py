from models.common.io import InputFromString

from ..parser import parse_players_starting_positions


def test_parse_players_starting_positions():
    file_content = """Player 1 starting position: 1
                      Player 2 starting position: 3"""
    positions = parse_players_starting_positions(InputFromString(file_content))
    assert positions == (1, 3)
