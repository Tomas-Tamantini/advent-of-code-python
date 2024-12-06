from typing import Iterator

from models.common.io import InputReader

from .xmas_present import XmasPresent


def parse_xmas_presents(input_reader: InputReader) -> Iterator[XmasPresent]:
    for line in input_reader.readlines():
        yield XmasPresent(*map(int, line.split("x")))
