from typing import TypeVar, Generic
from models.common.vectors import Vector2D
from .cube_navigator import CubeNavigator
from .board_navigator import BoardNavigator

T = TypeVar("T")


class CubeNet(Generic[T]):
    def __init__(
        self, edge_length: int, cube_faces_planar_positions: dict[T, Vector2D]
    ) -> None:
        self._edge_length = edge_length
        self._faces_to_positions = cube_faces_planar_positions
        self._positions_to_faces = {
            v: k for k, v in cube_faces_planar_positions.items()
        }

    def cube_navigator_to_board_navigator(
        self, cube_navigator: CubeNavigator
    ) -> BoardNavigator:
        cube_face = cube_navigator.cube_face
        relative_position = cube_navigator.relative_position
        facing = cube_navigator.facing
        cube_face_position = self._faces_to_positions[cube_face]
        board_position = cube_face_position * self._edge_length + relative_position
        return BoardNavigator(position=board_position, facing=facing)

    def board_navigator_to_cube_navigator(
        self, board_navigator: BoardNavigator
    ) -> CubeNavigator:
        facing = board_navigator.facing
        board_position = board_navigator.position
        face_position = Vector2D(
            board_position.x // self._edge_length, board_position.y // self._edge_length
        )
        cube_face = self._positions_to_faces[face_position]
        relative_position = board_position - face_position * self._edge_length
        return CubeNavigator(
            cube_face=cube_face, relative_position=relative_position, facing=facing
        )
