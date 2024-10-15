from typing import Iterator
from models.common.vectors import CardinalDirection
from models.common.io import InputReader
from .dig_plan import DiggerInstruction


def _parse_hexadecimal_instruction(line: str) -> DiggerInstruction:
    parts = line.split()
    number_repr = parts[2].replace("(", "").replace(")", "")
    hexa_number = int(number_repr[1:], 16)
    num_steps = hexa_number // 16
    direction = {
        0: CardinalDirection.EAST,
        1: CardinalDirection.SOUTH,
        2: CardinalDirection.WEST,
        3: CardinalDirection.NORTH,
    }[hexa_number % 16]
    return DiggerInstruction(direction, num_steps)


def _parse_decimal_instruction(line: str) -> DiggerInstruction:
    parts = line.split()
    direction = {
        "U": CardinalDirection.NORTH,
        "R": CardinalDirection.EAST,
        "D": CardinalDirection.SOUTH,
        "L": CardinalDirection.WEST,
    }[parts[0]]
    num_steps = int(parts[1])
    return DiggerInstruction(direction, num_steps)


def parse_dig_plan(
    input_reader: InputReader, parse_hexadecimal: bool
) -> Iterator[DiggerInstruction]:
    for line in input_reader.read_stripped_lines():
        if parse_hexadecimal:
            yield _parse_hexadecimal_instruction(line)
        else:
            yield _parse_decimal_instruction(line)
