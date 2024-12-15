from typing import Iterator

from models.common.io import CharacterGrid, InputReader
from models.common.vectors import CardinalDirection

from .logic import SingleWidthBox, Warehouse, WarehouseBoxes

_DIRECTIONS = {
    "<": CardinalDirection.WEST,
    ">": CardinalDirection.EAST,
    "^": CardinalDirection.NORTH,
    "v": CardinalDirection.SOUTH,
}


def parse_warehouse(input_reader: InputReader) -> Warehouse:
    lines = [
        line
        for line in input_reader.read_stripped_lines()
        if line[0] not in _DIRECTIONS
    ]
    joined_lines = "\n".join(lines)
    grid = CharacterGrid(joined_lines)
    boxes = {SingleWidthBox(pos) for pos in grid.positions_with_value("O")}
    return Warehouse(
        robot=next(grid.positions_with_value("@")),
        boxes=WarehouseBoxes(boxes),
        walls=set(grid.positions_with_value("#")),
    )


def parse_warehouse_robot_moves(
    input_reader: InputReader,
) -> Iterator[CardinalDirection]:
    for line in input_reader.read_stripped_lines():
        if line[0] in _DIRECTIONS:
            for char in line:
                yield _DIRECTIONS[char]
