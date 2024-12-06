from models.common.io import InputFromString

from ..parser import parse_cube_games


def test_parse_cube_games():
    file_content = """
                   Game 1: 4 red, 1 green, 15 blue; 6 green, 2 red
                   Game 2: 2 blue, 3 green; 5 blue
                   """
    input_reader = InputFromString(file_content)
    games = list(parse_cube_games(input_reader))
    assert len(games) == 2
    assert games[1].game_id == 2
    handfuls = list(games[0].handfuls)
    assert len(handfuls) == 2
    assert handfuls[0].amount_by_color == {"red": 4, "green": 1, "blue": 15}
