from dataclasses import dataclass

from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class LightBeam:
    position: Vector2D
    direction: CardinalDirection
