from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import HexagonalDirection


def _parse_rotated_hexagonal_directions_without_delimiters(
    line: str,
) -> Iterator[HexagonalDirection]:
    coord_map = {
        "se": HexagonalDirection.SOUTHEAST,
        "sw": HexagonalDirection.SOUTH,
        "nw": HexagonalDirection.NORTHWEST,
        "ne": HexagonalDirection.NORTH,
        "e": HexagonalDirection.NORTHEAST,
        "w": HexagonalDirection.SOUTHWEST,
    }
    current_idx = 0
    while current_idx < len(line):
        if line[current_idx] in coord_map:
            yield coord_map[line[current_idx]]
            current_idx += 1
        else:
            yield coord_map[line[current_idx : current_idx + 2]]
            current_idx += 2


def parse_rotated_hexagonal_directions(
    input_reader: InputReader,
) -> Iterator[list[HexagonalDirection]]:
    for line in input_reader.read_stripped_lines():
        yield list(_parse_rotated_hexagonal_directions_without_delimiters(line))
