from collections import defaultdict
from typing import Iterable, Iterator, Optional

from models.common.vectors import CardinalDirection, Vector2D


class AntisocialElves:
    def __init__(self, positions: set[Vector2D]) -> None:
        self._positions = positions.copy()
        self._num_elves_that_moved_last_round = len(positions)

    @property
    def num_elves_that_moved_last_round(self) -> int:
        return self._num_elves_that_moved_last_round

    @property
    def positions(self) -> set[Vector2D]:
        return self._positions

    def _neighbors(self, elf: Vector2D) -> Iterator[Vector2D]:
        for neighbor in elf.adjacent_positions(include_diagonals=True):
            if neighbor in self._positions:
                yield neighbor

    def _proposed_direction(
        self, elf: Vector2D, direction_priority: Iterable[CardinalDirection]
    ) -> Optional[CardinalDirection]:
        num_neighbors = 0
        forbidden_directions = set()

        for neighbor in self._neighbors(elf):
            offset = neighbor - elf
            num_neighbors += 1
            if offset.x > 0:
                forbidden_directions.add(CardinalDirection.EAST)
            elif offset.x < 0:
                forbidden_directions.add(CardinalDirection.WEST)
            if offset.y > 0:
                forbidden_directions.add(CardinalDirection.SOUTH)
            elif offset.y < 0:
                forbidden_directions.add(CardinalDirection.NORTH)

        if num_neighbors == 0:
            return None

        for direction in direction_priority:
            if direction not in forbidden_directions:
                return direction

    def move(self, direction_priority: Iterable[CardinalDirection]) -> None:
        proposed_positions = defaultdict(list)
        for elf in self._positions:
            direction = self._proposed_direction(elf, direction_priority)
            if direction is not None:
                proposed_positions[elf.move(direction, y_grows_down=True)].append(elf)

        self._num_elves_that_moved_last_round = 0
        for proposed_position, elves in proposed_positions.items():
            if len(elves) == 1:
                self._positions.remove(elves[0])
                self._positions.add(proposed_position)
                self._num_elves_that_moved_last_round += 1
