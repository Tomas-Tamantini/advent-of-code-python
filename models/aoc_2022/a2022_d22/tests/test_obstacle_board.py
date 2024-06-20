from unittest.mock import Mock
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import ObstacleBoard, BoardPiece


def test_obstacle_board_sends_piece_to_next_position_if_not_wall():
    mock_next_piece = BoardPiece(
        position=Vector2D(0, 0), facing=CardinalDirection.SOUTH
    )
    underlying_board = Mock()
    underlying_board.move_piece_forward.return_value = mock_next_piece
    piece = Mock()
    obstacle_board = ObstacleBoard(underlying_board, wall_positions=set())
    next_piece = obstacle_board.move_piece_forward(piece)
    assert next_piece == mock_next_piece
    underlying_board.move_piece_forward.assert_called_once_with(piece)


def test_obstacle_board_returns_same_piece_if_wall():
    wall_positions = {Vector2D(0, 0)}
    mock_next_piece = BoardPiece(
        position=Vector2D(0, 0), facing=CardinalDirection.SOUTH
    )
    underlying_board = Mock()
    underlying_board.move_piece_forward.return_value = mock_next_piece
    piece = Mock()
    obstacle_board = ObstacleBoard(underlying_board, wall_positions)
    next_piece = obstacle_board.move_piece_forward(piece)
    assert next_piece == piece
