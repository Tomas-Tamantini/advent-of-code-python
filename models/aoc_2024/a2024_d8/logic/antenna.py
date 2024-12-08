from dataclasses import dataclass

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class Antenna:
    frequency: chr
    position: Vector2D
