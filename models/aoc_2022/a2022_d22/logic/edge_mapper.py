from typing import Protocol
from models.common.vectors import Vector2D
from .cube_navigator import CubeNavigator
from .cube_net import CubeNet


class EdgeMapper(Protocol):
    @property
    def cube_net(self) -> CubeNet: ...

    def next_navigator_state(self, navigator: CubeNavigator) -> CubeNavigator: ...


class PacmanEdgeMapper:
    def __init__(self, cube_net: CubeNet):
        self._cube_net = cube_net

    @property
    def cube_net(self) -> CubeNet:
        return self._cube_net

    def _offset_vector(self, navigator: CubeNavigator) -> Vector2D:
        dx, dy = navigator.facing.offset()
        return Vector2D(dx, -dy)

    def _next_relative_position(self, navigator: CubeNavigator) -> Vector2D:
        offset_vector = self._offset_vector(navigator)
        multiplier = self._cube_net.edge_length - 1
        return navigator.relative_position - multiplier * offset_vector

    def _wrap_around_face(self, navigator: CubeNavigator):
        face_position = self._cube_net.face_position(navigator.cube_face)
        faces = (
            self._cube_net.faces_on_row(face_position.y)
            if navigator.facing.is_horizontal
            else self._cube_net.faces_on_column(face_position.x)
        )
        return min(
            faces,
            key=lambda face: self._cube_net.face_position(face).dot_product(
                self._offset_vector(navigator)
            ),
        )

    def next_navigator_state(self, navigator: CubeNavigator) -> CubeNavigator:
        face_position = self._cube_net.face_position(navigator.cube_face)
        new_face_position = face_position.move(navigator.facing, y_grows_down=True)
        new_face = self._cube_net.face_at(new_face_position)
        if new_face is None:
            new_face = self._wrap_around_face(navigator)
        new_relative_position = self._next_relative_position(navigator)
        return CubeNavigator(
            cube_face=new_face,
            relative_position=new_relative_position,
            facing=navigator.facing,
        )
