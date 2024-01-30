from typing import Iterator
from dataclasses import dataclass
from .cardinal_directions import CardinalDirection


@dataclass(frozen=True)
class Vector2D:
    x: int = 0
    y: int = 0

    def move(
        self,
        direction: CardinalDirection,
        num_steps: int = 1,
        y_grows_down: bool = False,
    ) -> "Vector2D":
        dx, dy = direction.offset()
        if y_grows_down:
            dy = -dy
        return Vector2D(self.x + dx * num_steps, self.y + dy * num_steps)

    def adjacent_positions(
        self, include_diagonals: bool = False
    ) -> Iterator["Vector2D"]:
        for direction in CardinalDirection:
            yield self.move(direction)
        if include_diagonals:
            for dx in (-1, 1):
                for dy in (-1, 1):
                    yield Vector2D(self.x + dx, self.y + dy)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> "Vector2D":
        return self * scalar
