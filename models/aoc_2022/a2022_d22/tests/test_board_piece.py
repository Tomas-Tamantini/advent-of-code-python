from models.common.vectors import CardinalDirection, TurnDirection, Vector2D

from ..logic import BoardPiece


def test_board_piece_turns_in_place():
    piece = BoardPiece(position=Vector2D(123, 321), facing=CardinalDirection.NORTH)
    assert piece.turn(TurnDirection.LEFT) == BoardPiece(
        position=Vector2D(123, 321), facing=CardinalDirection.WEST
    )


def test_board_piece_steps_forward_without_turning():
    piece = BoardPiece(position=Vector2D(123, 321), facing=CardinalDirection.NORTH)
    assert piece.step_forward() == BoardPiece(
        position=Vector2D(123, 320), facing=CardinalDirection.NORTH
    )
