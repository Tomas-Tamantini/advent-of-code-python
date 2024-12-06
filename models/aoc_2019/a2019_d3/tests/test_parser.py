from models.common.io import InputFromString
from models.common.vectors import CardinalDirection

from ..parser import parse_directions


def test_parse_directions():
    file_content = """R8,U5
                      U7,L6,D4"""
    directions = list(parse_directions(InputFromString(file_content)))
    assert directions == [
        [(CardinalDirection.EAST, 8), (CardinalDirection.NORTH, 5)],
        [
            (CardinalDirection.NORTH, 7),
            (CardinalDirection.WEST, 6),
            (CardinalDirection.SOUTH, 4),
        ],
    ]
