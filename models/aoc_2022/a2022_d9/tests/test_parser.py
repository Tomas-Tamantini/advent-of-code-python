from models.common.io import InputFromString
from models.common.vectors import CardinalDirection
from ..parser import parse_move_instructions


def test_parse_file_tree():
    input_reader = InputFromString(
        """
        R 4
        U 4
        L 3
        D 1
        """
    )
    instructions = list(parse_move_instructions(input_reader))
    assert instructions == [
        (CardinalDirection.EAST, 4),
        (CardinalDirection.NORTH, 4),
        (CardinalDirection.WEST, 3),
        (CardinalDirection.SOUTH, 1),
    ]
