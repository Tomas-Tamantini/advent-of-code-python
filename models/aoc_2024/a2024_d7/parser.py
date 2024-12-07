from typing import Iterator

from models.common.io import InputReader

from .logic import Equation


def _parse_equation(line: str) -> Equation:
    test_value, terms = line.split(":")
    return Equation(int(test_value), tuple(map(int, terms.split())))


def parse_equations(input_reader: InputReader) -> Iterator[Equation]:
    for line in input_reader.read_stripped_lines():
        yield _parse_equation(line)
