from dataclasses import dataclass
from models.common.vectors import Vector2D


@dataclass(frozen=True)
class CubeFace:
    walls: frozenset[Vector2D]
