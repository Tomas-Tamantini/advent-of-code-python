from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..parser import parse_racetrack


def test_parse_racetrack():
    file_content = """
                   S.#
                   #.E
                   """
    input_reader = InputFromString(file_content)
    track = parse_racetrack(input_reader)
    assert track._start == Vector2D(0, 0)
    assert track._end == Vector2D(2, 1)
    assert track._wall_positions == {Vector2D(2, 0), Vector2D(0, 1)}
    assert track._track_positions == {
        Vector2D(0, 0),
        Vector2D(1, 0),
        Vector2D(1, 1),
        Vector2D(2, 1),
    }
