from dataclasses import dataclass
from models.common.vectors import Vector3D


@dataclass(frozen=True)
class Hailstone:
    position: Vector3D
    velocity: Vector3D
