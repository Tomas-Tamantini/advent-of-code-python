from models.aoc_2016 import Keypad
from models.vectors import CardinalDirection


def test_keypad_starts_at_given_key():
    keypad = Keypad(initial_key=5)
    assert keypad.key == 5


def test_can_move_to_adjacent_keys():
    keypad = Keypad(initial_key=5)
    keypad.move_to_adjacent_key(CardinalDirection.NORTH)
    assert keypad.key == 2
    keypad.move_to_adjacent_key(CardinalDirection.EAST)
    assert keypad.key == 3
    keypad.move_to_adjacent_key(CardinalDirection.SOUTH)
    assert keypad.key == 6
    keypad.move_to_adjacent_key(CardinalDirection.WEST)
    assert keypad.key == 5


def test_cannot_move_outside_pad():
    keypad = Keypad(initial_key=1)
    keypad.move_to_adjacent_key(CardinalDirection.NORTH)
    assert keypad.key == 1
    keypad.move_to_adjacent_key(CardinalDirection.WEST)
    assert keypad.key == 1
    keypad.move_to_adjacent_key(CardinalDirection.SOUTH)
    assert keypad.key == 4
    keypad.move_to_adjacent_key(CardinalDirection.WEST)
    assert keypad.key == 4


def test_can_move_multiple_keys_in_one_go():
    keypad = Keypad(initial_key=5)
    keypad.move_multiple_keys([CardinalDirection.NORTH, CardinalDirection.EAST])
    assert keypad.key == 3
