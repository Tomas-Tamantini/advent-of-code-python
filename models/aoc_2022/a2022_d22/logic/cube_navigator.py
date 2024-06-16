from dataclasses import dataclass
from typing import TypeVar, Generic
from models.common.vectors import Vector2D, CardinalDirection

T = TypeVar("T")


@dataclass
class CubeNavigator(Generic[T]):
    cube_face: T
    relative_position: Vector2D
    facing: CardinalDirection

    def hit_wall(self) -> bool:
        return self.relative_position in self.cube_face.walls

    def is_about_to_leave_cube_face(self, edge_length: int) -> bool:
        new_position = self.relative_position.move(self.facing, y_grows_down=True)
        return (
            new_position.x < 0
            or new_position.y < 0
            or new_position.x >= edge_length
            or new_position.y >= edge_length
        )
