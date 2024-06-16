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

    def next_navigator_state(self, navigator: CubeNavigator) -> CubeNavigator:
        dx, dy = navigator.facing.offset()
        offset_vector = Vector2D(dx, -dy)
        new_relative_position = (
            navigator.relative_position
            - (self._cube_net.edge_length - 1) * offset_vector
        )

        face_position = self._cube_net.face_position(navigator.cube_face)
        faces = (
            self._cube_net.faces_on_row(face_position.y)
            if navigator.facing.is_horizontal
            else self._cube_net.faces_on_column(face_position.x)
        )

        new_face = min(
            faces,
            key=lambda face: self._cube_net.face_position(face).dot_product(
                offset_vector
            ),
        )

        return CubeNavigator(
            cube_face=new_face,
            relative_position=new_relative_position,
            facing=navigator.facing,
        )
