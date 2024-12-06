from typing import Iterator

from models.common.vectors import Vector2D

from .cube_navigator import CubeNavigator
from .cube_net import CubeNet


class PacmanEdgeMapper:
    def __init__(self, cube_net: CubeNet) -> None:
        self._cube_net = cube_net

    def _faces_on_row(self, row_idx: int) -> Iterator[Vector2D]:
        return (face for face in self._cube_net if face.y == row_idx)

    def _faces_on_column(self, column_idx: int) -> Iterator[Vector2D]:
        return (face for face in self._cube_net if face.x == column_idx)

    def _wrap_around(self, navigator: CubeNavigator) -> Vector2D:
        faces = (
            self._faces_on_row(navigator.face_planar_position.y)
            if navigator.facing.is_horizontal
            else self._faces_on_column(navigator.face_planar_position.x)
        )
        if navigator.facing in {navigator.facing.EAST, navigator.facing.SOUTH}:
            return min(faces)
        else:
            return max(faces)

    def _next_navigator_position(self, navigator: CubeNavigator) -> Vector2D:
        if (next_pos := navigator.next_position()) in self._cube_net:
            return next_pos
        else:
            return self._wrap_around(navigator)

    def next_navigator(self, navigator: CubeNavigator) -> CubeNavigator:
        return CubeNavigator(
            face_planar_position=self._next_navigator_position(navigator),
            facing=navigator.facing,
        )
