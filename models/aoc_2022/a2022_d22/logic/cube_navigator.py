from dataclasses import dataclass
from typing import TypeVar, Generic
from models.common.vectors import Vector2D, CardinalDirection

T = TypeVar("T")


@dataclass
class CubeNavigator(Generic[T]):
    cube_face: T
    relative_position: Vector2D
    facing: CardinalDirection
