from models.common.io import InputFromString
from models.common.vectors import Vector2D
from ..parser import parse_ash_valleys


def test_parse_ash_valleys():
    file_content = """
                   ...##....
                   .#.##.#..
                   .#....#..
                   .##..##..
                   ...##....
                   ..####.##
                   #..##..##
   
                   #..#
                   ..#.
                   """
    input_reader = InputFromString(file_content)
    valleys = list(parse_ash_valleys(input_reader))
    assert len(valleys) == 2
    assert valleys[0].width, valleys[0].height == (2, 3)
    assert valleys[1].width, valleys[1].height == (2, 3)
    assert valleys[1].get_tile(Vector2D(0, 0)) == "#"
    assert valleys[1].get_tile(Vector2D(3, 1)) == "."
    assert valleys[1].get_tile(Vector2D(3, 0)) == "#"
