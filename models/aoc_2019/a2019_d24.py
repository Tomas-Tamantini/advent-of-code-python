from typing import Hashable, Iterator, Optional
from dataclasses import dataclass
from models.vectors import Vector2D, CardinalDirection
from models.cellular_automata import (
    MultiStateCellVicinity,
    MultiState2DAutomaton,
    multi_state_automaton_next_state,
)
from models.progress_bar_protocol import ProgressBar

DEAD, ALIVE = 0, 1


def _bugs_automaton_rule(vicinity: MultiStateCellVicinity) -> Hashable:
    if (
        vicinity.center_cell_type == DEAD
        and 1 <= vicinity.num_neighbors_by_type(ALIVE) <= 2
    ) or (
        vicinity.center_cell_type == ALIVE
        and vicinity.num_neighbors_by_type(ALIVE) == 1
    ):
        return ALIVE
    else:
        return DEAD


class BugsAutomaton(MultiState2DAutomaton):
    def __init__(self, width: int, height: int) -> None:
        default_cell_type = DEAD
        super().__init__(
            default_cell_type, width, height, consider_diagonal_neighbors=False
        )

    def apply_rule(self, vicinity: MultiStateCellVicinity) -> Hashable:
        return _bugs_automaton_rule(vicinity)

    def next_live_cells(self, live_cells: set[Vector2D]) -> set[Vector2D]:
        cells = {c: ALIVE for c in live_cells}
        next_gen = self.next_state(cells)
        return {pos for pos, cell in next_gen.items() if cell == ALIVE}

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
            state = self.next_live_cells(state)


@dataclass(frozen=True)
class RecursiveTile:
    position: Vector2D
    level: int


class RecursiveBugsAutomaton:
    def __init__(self, width: int, height: int) -> None:
        self._height = height
        self._width = width
        self._center = Vector2D(width // 2, height // 2)

    @property
    def default_cell_type(self) -> int:
        return DEAD

    def is_within_bounds(self, cell: RecursiveTile) -> bool:
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

    def apply_rule(self, vicinity: MultiStateCellVicinity) -> int:
        return _bugs_automaton_rule(vicinity)

    def advance(
        self,
        initial_configuration_on_level_zero: set[Vector2D],
        num_steps: int,
        progress_bar: Optional[ProgressBar] = None,
    ) -> set[RecursiveTile]:
        current_state = {
            RecursiveTile(position, level=0): ALIVE
            for position in initial_configuration_on_level_zero
        }
        for current_step in range(num_steps):
            if progress_bar is not None:
                current_step += 1
                progress_bar.update(current_step, num_steps)
            current_state = multi_state_automaton_next_state(self, current_state)
        final_state = {cell for cell in current_state if current_state[cell] == ALIVE}
        return final_state
