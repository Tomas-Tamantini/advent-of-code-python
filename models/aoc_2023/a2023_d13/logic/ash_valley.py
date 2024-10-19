from models.common.io import CharacterGrid
from models.common.vectors import Vector2D


class AshValley:
    def __init__(self, grid: CharacterGrid) -> None:
        self._grid = grid

    @property
    def width(self) -> int:
        return self._grid.width

    @property
    def height(self) -> int:
        return self._grid.height

    def get_tile(self, position: Vector2D) -> chr:
        return self._grid.tiles[position]
