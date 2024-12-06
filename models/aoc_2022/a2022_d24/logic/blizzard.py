from dataclasses import dataclass

from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class Blizzard:
    initial_position: Vector2D
    direction: CardinalDirection
