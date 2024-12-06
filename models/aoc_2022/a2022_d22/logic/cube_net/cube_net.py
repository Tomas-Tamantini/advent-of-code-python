from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D


class CubeNet:
    def __init__(self, face_planar_positions: set[Vector2D]):
        self._face_planar_positions = face_planar_positions

    @property
    def face_planar_positions(self) -> set[Vector2D]:
        return self._face_planar_positions

    def directions_with_adjacent_faces(
        self, face_planar_position: Vector2D
    ) -> Iterator[CardinalDirection]:
        for direction in CardinalDirection:
            if (
                face_planar_position.move(direction, y_grows_down=True)
                in self._face_planar_positions
            ):
                yield direction

    def __contains__(self, face_planar_position: Vector2D) -> bool:
        return face_planar_position in self._face_planar_positions

    def __iter__(self):
        return iter(self._face_planar_positions)
