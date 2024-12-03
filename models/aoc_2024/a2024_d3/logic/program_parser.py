import re
from typing import Iterator
from .program_instructions import (
    ProgramInstruction,
    MultiplicationInstruction,
    DontInstruction,
    DoInstruction,
)


def _parse_instruction(program: str, match: re.Match[str]) -> ProgramInstruction:
    substring = program[match.start() : match.end()]
    if "mul" in substring:
        return MultiplicationInstruction(int(match.group(1)), int(match.group(2)))
    elif "don't" in substring:
        return DontInstruction()
    else:
        return DoInstruction()


def parse_program(program: str) -> Iterator[ProgramInstruction]:
    pattern_mult = r"mul\((\d{1,3}),(\d{1,3})\)"
    pattern_do = r"do\(\)"
    pattern_dont = r"don't\(\)"
    pattern = re.compile(f"{pattern_mult}|{pattern_do}|{pattern_dont}")
    for match in pattern.finditer(program):
        yield _parse_instruction(program, match)
