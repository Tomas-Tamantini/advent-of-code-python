from dataclasses import dataclass

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class HikingTrail:
    origin: Vector2D
    destination: Vector2D
