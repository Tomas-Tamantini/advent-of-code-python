from dataclasses import dataclass
from typing import Optional

from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class Crucible:
    position: Vector2D
    direction: Optional[CardinalDirection]
    num_steps_in_same_direction: int
