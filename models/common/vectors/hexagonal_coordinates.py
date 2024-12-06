from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Self


class HexagonalDirection(str, Enum):
    NORTH = "n"
    NORTHEAST = "ne"
    NORTHWEST = "nw"
    SOUTH = "s"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"


@dataclass(frozen=True)
class CanonicalHexagonalCoordinates:
    num_steps_north: int
    num_steps_northeast: int

    def num_steps_away_from_origin(self) -> int:
        if self.num_steps_north * self.num_steps_northeast >= 0:
            return abs(self.num_steps_north) + abs(self.num_steps_northeast)
        else:
            return max(abs(self.num_steps_north), abs(self.num_steps_northeast))

    def move(self, direction: HexagonalDirection, num_steps: int = 1) -> Self:
        north_offset = 0
        northeast_offset = 0
        if direction == HexagonalDirection.NORTH:
            north_offset = num_steps
        elif direction == HexagonalDirection.SOUTH:
            north_offset = -num_steps
        elif direction == HexagonalDirection.NORTHEAST:
            northeast_offset = num_steps
        elif direction == HexagonalDirection.SOUTHWEST:
            northeast_offset = -num_steps
        elif direction == HexagonalDirection.NORTHWEST:
            north_offset = num_steps
            northeast_offset = -num_steps
        elif direction == HexagonalDirection.SOUTHEAST:
            north_offset = -num_steps
            northeast_offset = num_steps
        else:
            raise ValueError(f"Invalid direction: {direction}")

        return CanonicalHexagonalCoordinates(
            num_steps_north=self.num_steps_north + north_offset,
            num_steps_northeast=self.num_steps_northeast + northeast_offset,
        )

    def adjacent_positions(self) -> Iterator[Self]:
        for direction in HexagonalDirection:
            yield self.move(direction)
