from models.common.vectors import CardinalDirection, Vector2D

from ..logic import TetrisPiece


def _example_piece():
    return TetrisPiece(shape=(Vector2D(0, 2), Vector2D(1, 0)), offset=Vector2D(10, 20))


def test_tetris_piece_positions_are_iterable():
    piece = _example_piece()
    assert set(piece.positions()) == {Vector2D(10, 22), Vector2D(11, 20)}


def test_tetris_piece_can_be_moved_in_all_four_directions():
    piece = _example_piece()
    moved_piece = piece.move(CardinalDirection.SOUTH)
    assert set(moved_piece.positions()) == {Vector2D(10, 21), Vector2D(11, 19)}
