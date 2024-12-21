from dataclasses import dataclass

from models.common.vectors import Vector2D

from .keypad_layout import KeypadLayout


@dataclass(frozen=True)
class KeypadRobot:
    initial_button: chr
    keypad_layout: KeypadLayout


NUMERIC_ROBOT = KeypadRobot(
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

DIRECTIONAL_ROBOT = KeypadRobot(
    initial_button="A",
    keypad_layout=KeypadLayout(
        {
            "^": Vector2D(1, 0),
            "A": Vector2D(2, 0),
            "<": Vector2D(0, 1),
            "v": Vector2D(1, 1),
            ">": Vector2D(2, 1),
        }
    ),
)
