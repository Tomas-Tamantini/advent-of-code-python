from typing import Optional, Iterator
from models.common.vectors import Vector2D


class FallingSand:
    def __init__(
        self,
        sand_pour_position: Vector2D,
        obstacle_positions: set[Vector2D],
        floor_y_coord: Optional[int] = None,
    ):
        self._sand_pour_position = sand_pour_position
        self._obstacle_positions = obstacle_positions
        self._resting_sand_positions = set()
        self._max_obstacle_depth = (
            max(o.y for o in obstacle_positions) if obstacle_positions else 0
        )
        self._steady_state_reached = False
        self._floor_y_coord = floor_y_coord

    def _cell_is_free(self, position: Vector2D) -> bool:
        if position in self._obstacle_positions:
            return False
        if position in self._resting_sand_positions:
            return False
        if self._floor_y_coord is None:
            return True
        return position.y < self._floor_y_coord

    def _free_cells_down(self, current_position: Vector2D) -> Iterator[Vector2D]:
        candidate_positions = (current_position + Vector2D(dx, 1) for dx in (0, -1, 1))
        for position in candidate_positions:
            if self._cell_is_free(position):
                yield position

    def _next_free_cell_down(self, current_position: Vector2D) -> Optional[Vector2D]:
        for free_cell in self._free_cells_down(current_position):
            return free_cell
        return None

    @property
    def max_obstacle_depth(self) -> int:
        return self._max_obstacle_depth

    @property
    def _max_depth(self) -> int:
        return (
            self._max_obstacle_depth
            if self._floor_y_coord is None
            else self._floor_y_coord
        )

    def _drop_next_grain(self):
        sand_positon = self._sand_pour_position
        while sand_positon.y < self._max_depth:
            free_cell_down = self._next_free_cell_down(sand_positon)
            if free_cell_down:
                sand_positon = free_cell_down
            else:
                self._resting_sand_positions.add(sand_positon)
                if sand_positon == self._sand_pour_position:
                    self._steady_state_reached = True
                return
        self._steady_state_reached = True

    def pour_until_steady_state(self) -> None:
        while not self._steady_state_reached:
            self._drop_next_grain()

    def pour_until_source_blocked(self) -> None:
        current_level = {self._sand_pour_position}
        next_level = set()
        while current_level:
            for position in current_level:
                self._resting_sand_positions.add(position)
                for free_cell_down in self._free_cells_down(position):
                    next_level.add(free_cell_down)
            current_level = next_level
            next_level = set()
        self._steady_state_reached = True

    @property
    def resting_sand_positions(self) -> set[Vector2D]:
        return self._resting_sand_positions
