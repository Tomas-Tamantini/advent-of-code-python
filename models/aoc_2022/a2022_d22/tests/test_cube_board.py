from unittest.mock import Mock
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import CubeBoard, BoardPiece, CubeNavigator


def test_cube_board_sends_piece_to_next_adjacent_position_if_not_leaving_cube_face():
    piece = BoardPiece(position=Vector2D(3, 6), facing=CardinalDirection.NORTH)
    cube_board = CubeBoard(cube_size=10, edge_mapper=Mock())
    next_piece = cube_board.move_piece_forward(piece)
    assert next_piece == BoardPiece(
        position=Vector2D(3, 5), facing=CardinalDirection.NORTH
    )


def test_cube_board_sends_piece_to_next_face_according_to_edge_mapper_if_leaving_current_cube_face():
    edge_mapper = Mock()
    edge_mapper.next_navigator.return_value = CubeNavigator(
        face_planar_position=Vector2D(1, 0),
        facing=CardinalDirection.NORTH,
    )
    piece = BoardPiece(position=Vector2D(9, 7), facing=CardinalDirection.EAST)
    cube_board = CubeBoard(cube_size=10, edge_mapper=edge_mapper)
    next_piece = cube_board.move_piece_forward(piece)
    assert next_piece == BoardPiece(
        position=Vector2D(17, 9), facing=CardinalDirection.NORTH
    )
