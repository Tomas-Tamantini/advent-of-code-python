from models.common.io import InputReader

from .string_scrambler import (
    LetterBasedRotationScrambler,
    LetterMoveScrambler,
    LetterSwapScrambler,
    MultiStepScrambler,
    PositionSwapScrambler,
    ReversionScrambler,
    RotationScrambler,
    StringScrambler,
)


def _parse_string_scrambler_function(line: str) -> StringScrambler:
    parse_map = {
        "swap position": lambda p: PositionSwapScrambler(
            position_a=int(p[2]), position_b=int(p[-1])
        ),
        "swap letter": lambda p: LetterSwapScrambler(letter_a=p[2], letter_b=p[-1]),
        "rotate left": lambda p: RotationScrambler(steps=-int(p[2])),
        "rotate right": lambda p: RotationScrambler(steps=int(p[2])),
        "rotate based on position of letter": lambda p: LetterBasedRotationScrambler(
            letter=p[-1]
        ),
        "reverse positions": lambda p: ReversionScrambler(
            start=int(p[2]), end=int(p[-1])
        ),
        "move position": lambda p: LetterMoveScrambler(
            origin=int(p[2]), destination=int(p[-1])
        ),
    }
    for key, value in parse_map.items():
        if key in line:
            parts = line.strip().split(" ")
            return value(parts)

    raise ValueError(f"Unknown instruction: {line.strip()}")


def parse_string_scrambler(input_reader: InputReader) -> MultiStepScrambler:
    scramblers = [
        _parse_string_scrambler_function(line) for line in input_reader.readlines()
    ]
    return MultiStepScrambler(scramblers)
