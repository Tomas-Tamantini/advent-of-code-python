from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import CardinalDirection


def parse_cardinal_direction_instructions(
    input_reader: InputReader,
) -> Iterator[list[CardinalDirection]]:
    direction_dict = {
        "U": CardinalDirection.NORTH,
        "R": CardinalDirection.EAST,
        "D": CardinalDirection.SOUTH,
        "L": CardinalDirection.WEST,
    }
    for line in input_reader.read_stripped_lines():
        yield [direction_dict[c] for c in line]
