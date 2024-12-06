from models.common.vectors import CardinalDirection

from ..keypad import Keypad


def keypad_factory(configuration: str = None, initial_key: chr = "5"):
    if not configuration:
        configuration = """123
                           456
                           789"""
    return Keypad(configuration, initial_key)


def test_keypad_starts_at_given_key():
    keypad = keypad_factory()
    assert keypad.key == "5"


def test_can_move_to_adjacent_keys():
    keypad = keypad_factory()
    keypad.move_to_adjacent_key(CardinalDirection.NORTH)
    assert keypad.key == "2"
    keypad.move_to_adjacent_key(CardinalDirection.EAST)
    assert keypad.key == "3"
    keypad.move_to_adjacent_key(CardinalDirection.SOUTH)
    assert keypad.key == "6"
    keypad.move_to_adjacent_key(CardinalDirection.WEST)
    assert keypad.key == "5"


def test_can_move_multiple_keys_in_one_go():
    keypad = keypad_factory()
    keypad.move_multiple_keys([CardinalDirection.NORTH, CardinalDirection.EAST])
    assert keypad.key == "3"


def test_cannot_move_outside_pad():
    keypad = keypad_factory(initial_key="1")
    keypad.move_to_adjacent_key(CardinalDirection.NORTH)
    assert keypad.key == "1"
    keypad.move_to_adjacent_key(CardinalDirection.WEST)
    assert keypad.key == "1"
    keypad.move_to_adjacent_key(CardinalDirection.SOUTH)
    assert keypad.key == "4"
    keypad.move_to_adjacent_key(CardinalDirection.WEST)
    assert keypad.key == "4"


def test_asterisk_is_considered_a_no_go_key():
    keypad = Keypad(
        configuration="""ABC
                         *DE
                         FGH""",
        initial_key="D",
    )
    keypad.move_to_adjacent_key(CardinalDirection.WEST)
    assert keypad.key == "D"
    keypad.move_multiple_keys(
        [CardinalDirection.SOUTH, CardinalDirection.WEST, CardinalDirection.NORTH]
    )
    assert keypad.key == "F"
