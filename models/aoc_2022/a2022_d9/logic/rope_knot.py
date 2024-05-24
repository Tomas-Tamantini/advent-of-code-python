from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class RopeKnot:
    position: Vector2D

    def move(self, direction: CardinalDirection) -> "RopeKnot":
        return RopeKnot(self.position.move(direction))

    def pull(self, other: "RopeKnot") -> "RopeKnot":
        diff = self.position - other.position
        if abs(diff.x) <= 1 and abs(diff.y) <= 1:
            return other
        dx = diff.x // abs(diff.x) if diff.x != 0 else 0
        dy = diff.y // abs(diff.y) if diff.y != 0 else 0
        return RopeKnot(other.position + Vector2D(dx, dy))
