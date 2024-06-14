from unittest.mock import Mock
from models.common.vectors import Vector2D, CardinalDirection, TurnDirection
from ..logic import TurnInstruction, MoveForwardInstruction, BoardNavigator


def test_turn_instruction_turns_navigator_in_place():
    navigator = BoardNavigator(position=Vector2D(0, 0), facing=CardinalDirection.NORTH)
    instruction = TurnInstruction(turn_direction=TurnDirection.RIGHT)
    board = Mock()
    new_navigator = instruction.execute(navigator, board)
    assert new_navigator == BoardNavigator(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST
    )


def test_move_forward_moves_navigator_to_permitted_position_on_board():
    navigator = BoardNavigator(position=Vector2D(0, 0), facing=CardinalDirection.WEST)
    instruction = MoveForwardInstruction(num_steps=3)
    board = Mock()
    board.next_position.return_value = Vector2D(123, 321)
    new_navigator = instruction.execute(navigator, board)
    assert new_navigator == BoardNavigator(
        position=Vector2D(123, 321), facing=CardinalDirection.WEST
    )
    board.next_position.assert_called_once_with(navigator, 3)
