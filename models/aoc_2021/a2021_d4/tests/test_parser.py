from models.common.io import InputFromString

from ..parser import parse_bingo_game_and_numbers_to_draw


def test_parse_bingo_game_and_numbers_to_draw():
    file_content = """
                   7,4,9,15

                   22 13 17
                   8  2  23
                   21 9  14

                   10 1  3
                   12 7  19
                   5  16 2
                   """
    game, numbers_to_draw = parse_bingo_game_and_numbers_to_draw(
        InputFromString(file_content)
    )
    assert numbers_to_draw == [7, 4, 9, 15]
    assert len(game.boards) == 2
    assert game.boards[0].num_rows == 3
    assert game.boards[0].num_columns == 3
