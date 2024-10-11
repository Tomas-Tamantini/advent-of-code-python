from models.common.io import CharacterGrid
from models.common.vectors import Vector2D


class CityMap:
    def __init__(self, grid: CharacterGrid):
        self._grid = grid
        self._final_position = Vector2D(grid.width - 1, grid.height - 1)

    @property
    def final_position(self) -> Vector2D:
        return self._final_position

    def is_within_bounds(self, position: Vector2D) -> bool:
        return (
            0 <= position.x < self._grid.width and 0 <= position.y < self._grid.height
        )

    def heat_loss_at(self, position: Vector2D) -> int:
        return int(self._grid.tiles[position])
