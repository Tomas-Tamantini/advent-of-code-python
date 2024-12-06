from unittest.mock import Mock

from models.common.vectors import CardinalDirection, TurnDirection, Vector2D

from ..logic import BoardPiece, MoveForwardInstruction, TurnInstruction


def test_turn_instruction_turns_piece_in_place():
    piece = BoardPiece(position=Vector2D(0, 0), facing=CardinalDirection.NORTH)
    instruction = TurnInstruction(turn_direction=TurnDirection.RIGHT)
    new_piece = instruction.execute(piece, board=None)
    assert new_piece == BoardPiece(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST
    )


def test_move_forward_moves_piece_to_next_position_on_board_once_for_each_step():
    piece = BoardPiece(position=Vector2D(0, 0), facing=CardinalDirection.SOUTH)
    instruction = MoveForwardInstruction(num_steps=3)
    board = Mock()
    board.move_piece_forward = lambda piece: BoardPiece(
        position=piece.position.move(CardinalDirection.EAST), facing=piece.facing
    )
    new_piece = instruction.execute(piece, board)
    assert new_piece == BoardPiece(
        position=Vector2D(3, 0), facing=CardinalDirection.SOUTH
    )


def test_move_forward_stops_when_piece_is_halted():
    piece = BoardPiece(position=Vector2D(0, 0), facing=CardinalDirection.SOUTH)
    mock_next_piece = BoardPiece(
        position=Vector2D(123, 321), facing=CardinalDirection.NORTH
    )
    instruction = MoveForwardInstruction(num_steps=1_000_000_000)
    board = Mock()
    board.move_piece_forward.return_value = mock_next_piece
    new_piece = instruction.execute(piece, board)
    assert new_piece == mock_next_piece
