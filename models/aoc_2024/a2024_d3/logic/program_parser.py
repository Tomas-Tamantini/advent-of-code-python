import re
from typing import Iterator
from .multiplication_operation import MultiplicationOperation


def parse_program(program: str) -> Iterator[MultiplicationOperation]:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    for match in pattern.finditer(program):
        yield MultiplicationOperation(int(match.group(1)), int(match.group(2)))
