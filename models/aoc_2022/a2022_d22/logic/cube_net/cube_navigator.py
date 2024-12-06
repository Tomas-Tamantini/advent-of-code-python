from dataclasses import dataclass

from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class CubeNavigator:
    face_planar_position: Vector2D
    facing: CardinalDirection

    def next_position(self) -> Vector2D:
        return self.face_planar_position.move(self.facing, y_grows_down=True)
