from models.common.io import InputFromString
from models.common.vectors import CardinalDirection
from ..parser import parse_cardinal_direction_instructions


def test_parse_cardinal_direction_instructions():
    input_reader = InputFromString(
        """
        UR
        D
        LLD
        """
    )
    directions = list(parse_cardinal_direction_instructions(input_reader))
    assert directions == [
        [CardinalDirection.NORTH, CardinalDirection.EAST],
        [CardinalDirection.SOUTH],
        [CardinalDirection.WEST, CardinalDirection.WEST, CardinalDirection.SOUTH],
    ]
