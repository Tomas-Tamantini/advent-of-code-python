from typing import Iterator

from models.common.io import InputReader


def parse_available_patterns(input_reader: InputReader) -> Iterator[str]:
    for line in input_reader.read_stripped_lines():
        if "," in line:
            yield from line.split(", ")


def parse_desired_designs(input_reader: InputReader) -> Iterator[str]:
    for line in input_reader.read_stripped_lines():
        if "," not in line:
            yield line
