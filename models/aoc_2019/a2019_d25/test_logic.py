import pytest

from models.common.vectors import CardinalDirection

from .logic import (
    DroidInput,
    DroidOutput,
    DropCommand,
    InventoryCommand,
    MoveCommand,
    TakeCommand,
)


def test_move_command_is_converted_to_proper_string():
    assert str(MoveCommand(CardinalDirection.NORTH)) == "north"
    assert str(MoveCommand(CardinalDirection.EAST)) == "east"
    assert str(MoveCommand(CardinalDirection.SOUTH)) == "south"
    assert str(MoveCommand(CardinalDirection.WEST)) == "west"


def test_take_command_is_converted_to_proper_string():
    assert str(TakeCommand("green ball")) == "take green ball"


def test_drop_command_is_converted_to_proper_string():
    assert str(DropCommand("green ball")) == "drop green ball"


def test_inventory_command_is_converted_to_proper_string():
    assert str(InventoryCommand()) == "inv"


def test_droid_input_converts_command_to_ascii_sequence_followed_by_new_line():
    droid_input = DroidInput()
    droid_input.give_command(MoveCommand(CardinalDirection.NORTH))
    expected_sequence = "north\n"
    for letter in expected_sequence:
        assert droid_input.read() == ord(letter)


def test_droid_input_enqueus_commands():
    droid_input = DroidInput()
    droid_input.give_command(MoveCommand(CardinalDirection.NORTH))
    droid_input.give_command(InventoryCommand())
    expected_sequence = "north\ninv\n"
    for letter in expected_sequence:
        assert droid_input.read() == ord(letter)


def test_droid_input_raises_value_error_if_reading_from_empty_queue():
    droid_input = DroidInput()
    with pytest.raises(ValueError):
        droid_input.read()


def test_droid_output_accumulates_output_ascii_values_until_new_line():
    class _MockHandler:
        def __init__(self) -> None:
            self.output_line = None

        def handle_new_output_line(self, output_line: str) -> None:
            self.output_line = output_line

    output_handler = _MockHandler()
    droid_output = DroidOutput(output_handler)
    droid_output.write(ord("a"))
    assert output_handler.output_line is None
    droid_output.write(ord("b"))
    droid_output.write(ord("c"))
    droid_output.write(ord("\n"))
    assert output_handler.output_line == "abc"
    droid_output.write(ord("d"))
    droid_output.write(ord("\n"))
    assert output_handler.output_line == "d"
