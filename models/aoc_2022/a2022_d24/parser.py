from typing import Iterator
from models.common.io import InputReader, CharacterGrid
from models.common.vectors import CardinalDirection
from .logic import Blizzard, BlizzardValley


def _parse_blizzards(grid: CharacterGrid) -> Iterator[Blizzard]:
    directions = {
        ">": CardinalDirection.EAST,
        "<": CardinalDirection.WEST,
        "^": CardinalDirection.NORTH,
        "v": CardinalDirection.SOUTH,
    }
    for direction_chr, direction in directions.items():
        for pos in grid.positions_with_value(direction_chr):
            yield Blizzard(initial_position=pos, direction=direction)


def parse_blizzard_valley(input_reader: InputReader) -> BlizzardValley:
    grid = CharacterGrid(input_reader.read())
    open_positions = set(grid.positions_with_value("."))
    entrance_pos = min(open_positions, key=lambda pos: pos.y)
    exit_pos = max(open_positions, key=lambda pos: pos.y)
    blizzards = set(_parse_blizzards(grid))
    return BlizzardValley(grid.height, grid.width, entrance_pos, exit_pos, blizzards)
