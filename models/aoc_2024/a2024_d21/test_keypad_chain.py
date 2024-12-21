from models.common.vectors import Vector2D

from .logic import KeypadLayout, KeypadRobot, min_num_keypad_presses

_code_robot = KeypadRobot(
    initial_button="A",
    keypad_layout=KeypadLayout(
        {
            "7": Vector2D(0, 0),
            "8": Vector2D(1, 0),
            "9": Vector2D(2, 0),
            "4": Vector2D(0, 1),
            "5": Vector2D(1, 1),
            "6": Vector2D(2, 1),
            "1": Vector2D(0, 2),
            "2": Vector2D(1, 2),
            "3": Vector2D(2, 2),
            "0": Vector2D(1, 3),
            "A": Vector2D(2, 3),
        }
    ),
)


def test_min_num_keypad_presses_with_no_directional_robots():
    assert min_num_keypad_presses(code="029A", code_robot=_code_robot) == 12
