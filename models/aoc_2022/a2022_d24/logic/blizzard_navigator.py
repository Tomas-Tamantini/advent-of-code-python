from typing import Iterator
from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class BlizzardNavigator:
    position: Vector2D
    time: int

    def _next_possible_positions(self) -> Iterator[Vector2D]:
        yield self.position
        for direction in (
            CardinalDirection.SOUTH,
            CardinalDirection.EAST,
            CardinalDirection.NORTH,
            CardinalDirection.WEST,
        ):
            yield self.position.move(direction)

    def next_states(self) -> Iterator["BlizzardNavigator"]:
        for position in self._next_possible_positions():
            yield BlizzardNavigator(position=position, time=self.time + 1)
