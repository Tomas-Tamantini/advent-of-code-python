from models.common.io import CharacterGrid
from models.common.vectors import CardinalDirection

from .logic import DirectedMaze


def parse_forest_map(grid: CharacterGrid, consider_slopes: bool) -> DirectedMaze:
    symbols = (
        {
            "^": CardinalDirection.NORTH,
            ">": CardinalDirection.EAST,
            "v": CardinalDirection.SOUTH,
            "<": CardinalDirection.WEST,
            ".": None,
        }
        if consider_slopes
        else {symbol: None for symbol in "^>v<."}
    )
    maze = DirectedMaze()
    for symbol, direction in symbols.items():
        for tile in grid.positions_with_value(symbol):
            maze.add_tile(tile, direction)
    return maze
