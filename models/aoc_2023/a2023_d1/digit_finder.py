from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass(frozen=True)
class Digit:
    position: int
    value: int


def _spelled_out_digit(sequence: str, position: int) -> Optional[int]:
    spelled = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    for word, value in spelled.items():
        if sequence[position:].startswith(word):
            return value


def find_digits(sequence: str, include_spelled_out: bool = False) -> Iterator[Digit]:
    for position, char in enumerate(sequence):
        if char.isdigit():
            yield Digit(position, int(char))
        elif include_spelled_out and (
            digit_value := _spelled_out_digit(sequence, position)
        ):
            yield Digit(position, digit_value)
