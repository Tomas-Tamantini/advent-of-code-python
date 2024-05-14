from dataclasses import dataclass
from models.vectors import Vector2D


@dataclass(frozen=True)
class Amphipod:
    position: Vector2D
    desired_room_index: int
    energy_spent_per_step: int
    num_moves: int = 0


@dataclass(frozen=True)
class AmphipodArrangement:
    amphipods: tuple[Amphipod, ...]
