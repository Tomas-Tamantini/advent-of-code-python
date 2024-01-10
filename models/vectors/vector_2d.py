from dataclasses import dataclass
from .cardinal_directions import CardinalDirection


@dataclass(frozen=True)
class Vector2D:
    x: int
    y: int

    def move(self, direction: CardinalDirection, num_steps: int = 1) -> "Vector2D":
        dx, dy = direction.offset()
        return Vector2D(self.x + dx * num_steps, self.y + dy * num_steps)
