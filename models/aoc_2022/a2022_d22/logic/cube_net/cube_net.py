from models.common.vectors import Vector2D


class CubeNet:
    def __init__(self, face_planar_positions: set[Vector2D]):
        self._face_planar_positions = face_planar_positions

    @property
    def face_planar_positions(self) -> set[Vector2D]:
        return self._face_planar_positions

    def __contains__(self, face_planar_position: Vector2D) -> bool:
        return face_planar_position in self._face_planar_positions

    def __iter__(self):
        return iter(self._face_planar_positions)
