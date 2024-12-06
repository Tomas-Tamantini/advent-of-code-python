from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class PatrolGuard:
    position: Vector2D
    direction: CardinalDirection
