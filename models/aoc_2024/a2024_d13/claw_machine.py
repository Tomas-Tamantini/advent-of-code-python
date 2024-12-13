from dataclasses import dataclass

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class ClawMachine:
    btn_a_offset: Vector2D
    btn_b_offset: Vector2D
    prize_location: Vector2D
