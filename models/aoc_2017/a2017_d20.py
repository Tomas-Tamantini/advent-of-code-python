from dataclasses import dataclass
from typing import Hashable


@dataclass(frozen=True)
class Particle:
    id: Hashable
    position: tuple[int, int, int]
    velocity: tuple[int, int, int]
    acceleration: tuple[int, int, int]
