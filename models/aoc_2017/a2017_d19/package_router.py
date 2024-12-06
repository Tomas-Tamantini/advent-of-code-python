from typing import Iterator

from models.common.graphs import explore_with_bfs
from models.common.vectors import CardinalDirection, Vector2D


class PackageRouter:
    def __init__(self, maze: list[str]) -> None:
        self._maze = maze
        self._width = len(self._maze[0])
        self._height = len(self._maze)
        self._num_steps = 0
        self._visited_letters = []

    @property
    def num_steps(self) -> int:
        return self._num_steps

    @property
    def visited_letters(self) -> list[str]:
        return self._visited_letters

    def _initial_state(self) -> tuple[Vector2D, CardinalDirection]:
        x = self._maze[0].index("|")
        return Vector2D(x, 0), CardinalDirection.NORTH

    def _is_valid_position(self, pos: Vector2D) -> bool:
        return (
            0 <= pos.x < self._width
            and 0 <= pos.y < self._height
            and self._get_cell(pos) != " "
        )

    def _get_cell(self, pos: Vector2D) -> str:
        return self._maze[pos.y][pos.x]

    def neighbors(
        self, state: tuple[Vector2D, CardinalDirection]
    ) -> Iterator[tuple[Vector2D, CardinalDirection]]:
        pos, direction = state
        new_pos = pos.move(direction)
        if not self._is_valid_position(new_pos):
            return
        if self._get_cell(new_pos) != "+":
            yield new_pos, direction
        else:
            candidate_new_directions = direction.turn_left(), direction.turn_right()
            for new_direction in candidate_new_directions:
                if self._is_valid_position(new_pos.move(new_direction)):
                    yield new_pos, new_direction

    def explore(self) -> None:
        self._num_steps = 0
        self._visited_letters = []
        initial_state = self._initial_state()
        for state, _ in explore_with_bfs(self, initial_state):
            self._num_steps += 1
            pos, _ = state
            if self._get_cell(pos).isalpha():
                self._visited_letters.append(self._get_cell(pos))
