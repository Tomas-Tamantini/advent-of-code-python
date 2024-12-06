import re
from typing import Iterator

from .program_instructions import (
    DoInstruction,
    DontInstruction,
    MultiplicationInstruction,
    ProgramInstruction,
)


def _parse_instruction(match: re.Match[str]) -> ProgramInstruction:
    if "mul" in match.group(0):
        return MultiplicationInstruction(int(match.group(1)), int(match.group(2)))
    elif match.group(0) == "do()":
        return DoInstruction()
    else:
        return DontInstruction()


def parse_program(program: str) -> Iterator[ProgramInstruction]:
    pattern_mult = r"mul\((\d{1,3}),(\d{1,3})\)"
    pattern_do = r"do\(\)"
    pattern_dont = r"don't\(\)"
    pattern = re.compile(f"{pattern_mult}|{pattern_do}|{pattern_dont}")
    for match in pattern.finditer(program):
        yield _parse_instruction(match)
