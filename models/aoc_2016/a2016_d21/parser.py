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
    parts = line.strip().split(" ")
    if "swap position" in line:
        return PositionSwapScrambler(
            position_a=int(parts[2]), position_b=int(parts[-1])
        )
    elif "swap letter" in line:
        return LetterSwapScrambler(letter_a=parts[2], letter_b=parts[-1])
    elif "rotate left" in line:
        steps = -int(parts[2])
        return RotationScrambler(steps=steps)
    elif "rotate right" in line:
        steps = int(parts[2])
        return RotationScrambler(steps=steps)
    elif "rotate based on position of letter" in line:
        return LetterBasedRotationScrambler(letter=parts[-1])
    elif "reverse positions" in line:
        return ReversionScrambler(start=int(parts[2]), end=int(parts[-1]))
    elif "move position" in line:
        origin = int(parts[2])
        destination = int(parts[-1])
        return LetterMoveScrambler(origin=origin, destination=destination)
    else:
        raise ValueError(f"Unknown instruction: {line.strip()}")


def parse_string_scrambler(input_reader: InputReader) -> MultiStepScrambler:
    scramblers = [
        _parse_string_scrambler_function(line) for line in input_reader.readlines()
    ]
    return MultiStepScrambler(scramblers)
