from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class BoardNavigator:
    position: Vector2D
    facing: CardinalDirection
