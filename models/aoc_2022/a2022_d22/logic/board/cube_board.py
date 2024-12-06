from models.common.vectors import CardinalDirection, TurnDirection, Vector2D

from ..board_piece import BoardPiece
from ..cube_net import CubeNavigator, EdgeMapper


class CubeBoard:
    def __init__(self, cube_size: int, edge_mapper: EdgeMapper) -> None:
        self._cube_size = cube_size
        self._edge_mapper = edge_mapper

    def _face_planar_position(self, position: Vector2D) -> Vector2D:
        return Vector2D(
            position.x // self._cube_size,
            position.y // self._cube_size,
        )

    def _absolute_position(self, face_planar_position: Vector2D) -> Vector2D:
        return Vector2D(
            face_planar_position.x * self._cube_size,
            face_planar_position.y * self._cube_size,
        )

    def _is_about_to_leave_cube_face(self, piece: BoardPiece) -> bool:
        current_face = self._face_planar_position(piece.position)
        next_face = self._face_planar_position(piece.step_forward().position)
        return current_face != next_face

    def _next_relative_position(
        self, piece: BoardPiece, next_facing: CardinalDirection
    ) -> Vector2D:
        x = piece.position.x % self._cube_size
        y = piece.position.y % self._cube_size
        direction = piece.facing
        while direction != next_facing:
            x, y = y, self._cube_size - 1 - x
            direction = direction.turn(TurnDirection.LEFT)
        offset = Vector2D(x, y).move(direction, y_grows_down=True)
        return Vector2D(offset.x % self._cube_size, offset.y % self._cube_size)

    def _go_to_next_face(self, piece: BoardPiece) -> BoardPiece:
        current_cube_navigator = CubeNavigator(
            face_planar_position=self._face_planar_position(piece.position),
            facing=piece.facing,
        )
        next_cube_navigator = self._edge_mapper.next_navigator(current_cube_navigator)
        offset = self._next_relative_position(piece, next_cube_navigator.facing)
        next_face_position = self._absolute_position(
            next_cube_navigator.face_planar_position
        )
        return BoardPiece(
            position=next_face_position + offset,
            facing=next_cube_navigator.facing,
        )

    def move_piece_forward(self, piece: BoardPiece) -> BoardPiece:
        if not self._is_about_to_leave_cube_face(piece):
            return piece.step_forward()
        else:
            return self._go_to_next_face(piece)
