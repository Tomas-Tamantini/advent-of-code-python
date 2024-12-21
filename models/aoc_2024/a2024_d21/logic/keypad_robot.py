from dataclasses import dataclass

from .keypad_layout import KeypadLayout


@dataclass(frozen=True)
class KeypadRobot:
    initial_button: chr
    keypad_layout: KeypadLayout
