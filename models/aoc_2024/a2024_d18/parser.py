from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Vector2D


def parse_byte_positions(input_reader: InputReader) -> Iterator[Vector2D]:
    for line in input_reader.read_stripped_lines():
        x, y = map(int, line.split(","))
        yield Vector2D(x, y)
