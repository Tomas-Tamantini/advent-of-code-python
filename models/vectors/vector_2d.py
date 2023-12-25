from dataclasses import dataclass
from .cardinal_directions import CardinalDirection


@dataclass(frozen=True)
class Vector2D:
    x: int
    y: int

    def move(self, direction: CardinalDirection) -> "Vector2D":
        if direction == CardinalDirection.NORTH:
            return Vector2D(self.x, self.y + 1)
        elif direction == CardinalDirection.EAST:
            return Vector2D(self.x + 1, self.y)
        elif direction == CardinalDirection.SOUTH:
            return Vector2D(self.x, self.y - 1)
        else:
            return Vector2D(self.x - 1, self.y)
