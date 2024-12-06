from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import CardinalDirection


def parse_wind_directions(input_reader: InputReader) -> Iterator[CardinalDirection]:
    yield from (
        CardinalDirection.EAST if c == ">" else CardinalDirection.WEST
        for c in input_reader.read().strip()
    )
