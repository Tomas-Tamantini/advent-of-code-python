from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import CardinalDirection


def parse_directions(
    input_reader: InputReader,
) -> Iterator[list[tuple[CardinalDirection, int]]]:
    direction_dict = {
        "U": CardinalDirection.NORTH,
        "R": CardinalDirection.EAST,
        "D": CardinalDirection.SOUTH,
        "L": CardinalDirection.WEST,
    }

    for line in input_reader.readlines():
        yield [
            (direction_dict[part.strip()[0]], int(part.strip()[1:]))
            for part in line.strip().split(",")
        ]
