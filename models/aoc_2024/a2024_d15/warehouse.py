from dataclasses import dataclass

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class Warehouse:
    robot: Vector2D
    boxes: set[Vector2D]
    walls: set[Vector2D]
