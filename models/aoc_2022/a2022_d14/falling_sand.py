from models.common.vectors import Vector2D
from typing import Optional


class FallingSand:
    def __init__(self, sand_pour_position: Vector2D, obstacle_positions: set[Vector2D]):
        self._sand_pour_position = sand_pour_position
        self._obstacle_positions = obstacle_positions
        self._resting_sand_positions = set()
        self._max_depth = (
            max(o.y for o in obstacle_positions) if obstacle_positions else 0
        )
        self._steady_state_reached = False

    def _cell_is_free(self, position: Vector2D) -> bool:
        return (
            position not in self._obstacle_positions
            and position not in self._resting_sand_positions
        )

    def _next_free_cell_down(self, current_position: Vector2D) -> Optional[Vector2D]:
        candidate_positions = (current_position + Vector2D(dx, 1) for dx in (0, -1, 1))
        for position in candidate_positions:
            if self._cell_is_free(position):
                return position

    def _drop_next_grain(self):
        sand_positon = self._sand_pour_position
        while sand_positon.y < self._max_depth:
            free_cell_down = self._next_free_cell_down(sand_positon)
            if free_cell_down:
                sand_positon = free_cell_down
            else:
                self._resting_sand_positions.add(sand_positon)
                return
        self._steady_state_reached = True

    def pour_until_steady_state(self) -> None:
        while not self._steady_state_reached:
            self._drop_next_grain()

    @property
    def resting_sand_positions(self) -> set[Vector2D]:
        return self._resting_sand_positions
