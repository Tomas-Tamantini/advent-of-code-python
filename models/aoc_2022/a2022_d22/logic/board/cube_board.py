from models.common.vectors import Vector2D, CardinalDirection
from ..board_piece import BoardPiece
from ..cube_net import EdgeMapper, CubeNavigator


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

    def _go_to_next_face(self, piece: BoardPiece) -> BoardPiece:
        current_cube_navigator = CubeNavigator(
            face_planar_position=self._face_planar_position(piece.position),
            facing=piece.facing,
        )
        next_cube_navigator = self._edge_mapper.next_navigator(current_cube_navigator)
        next_face_position = self._absolute_position(
            next_cube_navigator.face_planar_position
        )
        aux = self._cube_size - 1
        aux_x = piece.position.x % self._cube_size
        aux_y = piece.position.y % self._cube_size
        previous_facing = piece.facing
        next_facing = next_cube_navigator.facing
        if next_facing == CardinalDirection.EAST:
            if previous_facing == CardinalDirection.EAST:
                y = aux_y
            elif previous_facing == CardinalDirection.WEST:
                y = aux - aux_y
            elif previous_facing == CardinalDirection.NORTH:
                y = aux_x
            else:
                y = aux - aux_x
            offset = Vector2D(0, y)
        elif next_facing == CardinalDirection.WEST:
            if previous_facing == CardinalDirection.EAST:
                y = aux - aux_y
            elif previous_facing == CardinalDirection.WEST:
                y = aux_y
            elif previous_facing == CardinalDirection.NORTH:
                y = aux - aux_x
            else:
                y = aux_x
            offset = Vector2D(aux, y)
        elif next_facing == CardinalDirection.NORTH:
            if previous_facing == CardinalDirection.EAST:
                x = aux_y
            elif previous_facing == CardinalDirection.WEST:
                x = aux - aux_y
            elif previous_facing == CardinalDirection.NORTH:
                x = aux_x
            else:
                x = aux - aux_x
            offset = Vector2D(x, aux)
        else:
            if previous_facing == CardinalDirection.EAST:
                x = aux - aux_y
            elif previous_facing == CardinalDirection.WEST:
                x = aux_y
            elif previous_facing == CardinalDirection.NORTH:
                x = aux - aux_x
            else:
                x = aux_x
            offset = Vector2D(x, 0)
        return BoardPiece(next_face_position + offset, next_facing)

    def move_piece_forward(self, piece: BoardPiece) -> BoardPiece:
        if not self._is_about_to_leave_cube_face(piece):
            return piece.step_forward()
        else:
            return self._go_to_next_face(piece)
