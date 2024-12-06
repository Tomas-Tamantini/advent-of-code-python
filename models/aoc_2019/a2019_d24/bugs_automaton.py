from dataclasses import dataclass
from typing import Iterator, Optional

from models.common.cellular_automata import (
    Bounded2DAutomaton,
    TwoStateCellVicinity,
    two_state_automaton_next_state,
)
from models.common.io import ProgressBar
from models.common.vectors import CardinalDirection, Vector2D


def _bugs_automaton_rule(vicinity: TwoStateCellVicinity) -> bool:
    return (
        not vicinity.center_cell_is_alive and 1 <= vicinity.num_alive_neighbors() <= 2
    ) or (vicinity.center_cell_is_alive and vicinity.num_alive_neighbors() == 1)


class BugsAutomaton(Bounded2DAutomaton):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height, consider_diagonal_neighbors=False)

    @staticmethod
    def cell_is_alive_in_next_generation(vicinity: TwoStateCellVicinity) -> bool:
        return _bugs_automaton_rule(vicinity)

    def next_state(self, live_cells: set[Vector2D]) -> set[Vector2D]:
        return two_state_automaton_next_state(self, live_cells)

    def biodiversity_rating(self, live_cells: set[Vector2D]) -> int:
        return sum(2 ** (c.y * self._width + c.x) for c in live_cells)

    def first_pattern_to_appear_twice(
        self, initial_configuration: set[Vector2D]
    ) -> set[Vector2D]:
        seen = set()
        state = initial_configuration
        while True:
            if frozenset(state) in seen:
                return state
            seen.add(frozenset(state))
            state = self.next_state(state)


@dataclass(frozen=True)
class RecursiveTile:
    position: Vector2D
    level: int


class RecursiveBugsAutomaton:
    def __init__(self, width: int, height: int) -> None:
        self._height = height
        self._width = width
        self._center = Vector2D(width // 2, height // 2)

    @staticmethod
    def is_within_bounds(cell: RecursiveTile) -> bool:
        return True

    def _is_center(self, position: Vector2D) -> bool:
        return position == self._center

    def _central_neighbors(
        self, direction: CardinalDirection, level: int
    ) -> Iterator[RecursiveTile]:
        new_level = level - 1
        if direction.is_horizontal:
            x_coord = 0 if direction == CardinalDirection.EAST else self._width - 1
            for i in range(self._height):
                yield RecursiveTile(Vector2D(x_coord, i), new_level)
        else:
            y_coord = 0 if direction == CardinalDirection.NORTH else self._height - 1
            for i in range(self._width):
                yield RecursiveTile(Vector2D(i, y_coord), new_level)

    def neighbors(self, cell: RecursiveTile) -> Iterator[RecursiveTile]:
        for direction in CardinalDirection:
            neighbor = cell.position.move(direction)
            if neighbor.x < 0:
                yield RecursiveTile(self._center - Vector2D(1, 0), cell.level + 1)
            elif neighbor.y < 0:
                yield RecursiveTile(self._center - Vector2D(0, 1), cell.level + 1)
            elif neighbor.x >= self._width:
                yield RecursiveTile(self._center + Vector2D(1, 0), cell.level + 1)
            elif neighbor.y >= self._height:
                yield RecursiveTile(self._center + Vector2D(0, 1), cell.level + 1)
            elif neighbor == self._center:
                yield from self._central_neighbors(direction, cell.level)
            else:
                yield RecursiveTile(neighbor, cell.level)

    @staticmethod
    def cell_is_alive_in_next_generation(vicinity: TwoStateCellVicinity) -> bool:
        return _bugs_automaton_rule(vicinity)

    def advance(
        self,
        initial_configuration_on_level_zero: set[Vector2D],
        num_steps: int,
        progress_bar: Optional[ProgressBar] = None,
    ) -> set[RecursiveTile]:
        current_state = {
            RecursiveTile(position, level=0)
            for position in initial_configuration_on_level_zero
        }
        for current_step in range(num_steps):
            if progress_bar is not None:
                progress_bar.update(current_step, num_steps)
            current_state = two_state_automaton_next_state(self, current_state)
        return current_state
