from dataclasses import dataclass

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class WordPosition:
    start_position: Vector2D
    direction: Vector2D
