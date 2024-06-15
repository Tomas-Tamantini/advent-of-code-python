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
    navigator = BoardNavigator(position=Vector2D(0, 0), facing=CardinalDirection.SOUTH)
    instruction = MoveForwardInstruction(num_steps=3)
    board = Mock()
    new_navigator_return_value = BoardNavigator(
        position=Vector2D(123, 321), facing=CardinalDirection.SOUTH
    )
    board.move_navigator_forward.return_value = new_navigator_return_value
    new_navigator = instruction.execute(navigator, board)
    assert new_navigator == new_navigator_return_value
    board.move_navigator_forward.assert_called_once_with(navigator, 3)
