from typing import Iterator

from models.common.io import InputReader


def parse_connections(input_reader: InputReader) -> Iterator[tuple[str, str]]:
    for line in input_reader.read_stripped_lines():
        yield tuple(line.split("-"))
