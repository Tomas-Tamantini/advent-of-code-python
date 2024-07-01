from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Digit:
    position: int
    value: int


def find_digits(sequence: str) -> Iterator[Digit]:
    for position, char in enumerate(sequence):
        if char.isdigit():
            yield Digit(position, int(char))
