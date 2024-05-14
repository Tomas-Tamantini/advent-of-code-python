from dataclasses import dataclass
from models.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class BurrowRoom:
    back_position: Vector2D
    orientation: CardinalDirection


@dataclass(frozen=True)
class BurrowHallway:
    start_position: Vector2D
    orientation: CardinalDirection
    length: int


@dataclass(frozen=True)
class AmphipodBurrow:
    rooms: tuple[BurrowRoom, ...]
    hallway: BurrowHallway
