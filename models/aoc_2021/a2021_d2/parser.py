from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import CardinalDirection
from .submarine import (
    SubmarineNavigationInstruction,
    MoveSubmarineInstruction,
    IncrementAimInstruction,
    MoveSubmarineWithAimInstruction,
)


def _parse_navigation_instruction_for_submarine_without_aim(
    line: str,
) -> SubmarineNavigationInstruction:
    directions = {
        "forward": CardinalDirection.EAST,
        "up": CardinalDirection.NORTH,
        "down": CardinalDirection.SOUTH,
    }
    parts = line.split()
    return MoveSubmarineInstruction(directions[parts[0]], int(parts[1]))


def _parse_navigation_instruction_for_submarine_with_aim(
    line: str,
) -> SubmarineNavigationInstruction:
    instruction, amount = line.split()
    amount = int(amount)
    if "down" in instruction:
        return IncrementAimInstruction(amount)
    elif "up" in instruction:
        return IncrementAimInstruction(-amount)
    elif "forward" in instruction:
        return MoveSubmarineWithAimInstruction(amount)
    else:
        raise ValueError(f"Unknown submarine navigation instruction: {line}")


def parse_submarine_navigation_instructions(
    input_reader: InputReader, submarine_has_aim: bool
) -> Iterator[SubmarineNavigationInstruction]:
    for line in input_reader.read_stripped_lines():

        if submarine_has_aim:
            yield _parse_navigation_instruction_for_submarine_with_aim(line)
        else:
            yield _parse_navigation_instruction_for_submarine_without_aim(line)
