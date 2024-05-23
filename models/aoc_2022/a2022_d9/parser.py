from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import CardinalDirection


def parse_move_instructions(
    input_reader: InputReader,
) -> Iterator[tuple[CardinalDirection, int]]:
    char_to_dir = {
        "U": CardinalDirection.NORTH,
        "D": CardinalDirection.SOUTH,
        "L": CardinalDirection.WEST,
        "R": CardinalDirection.EAST,
    }
    for line in input_reader.read_stripped_lines():
        char, distance = line.split()
        yield char_to_dir[char], int(distance)
