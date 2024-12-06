from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..parser import parse_obstacles


def test_parse_obstacles():
    input_reader = InputFromString(
        """
        498,4 -> 498,6 -> 496,6
        503,4 -> 502,4 -> 502,9 -> 494,9
        """
    )
    positions = set(parse_obstacles(input_reader))
    assert len(positions) == 20
    assert Vector2D(496, 9) in positions
    assert Vector2D(498, 5)
