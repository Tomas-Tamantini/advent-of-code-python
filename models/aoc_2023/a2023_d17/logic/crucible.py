from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class Crucible:
    position: Vector2D
    direction: CardinalDirection
    num_steps_in_same_direction: int
