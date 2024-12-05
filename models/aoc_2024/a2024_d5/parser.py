from typing import Iterator
from models.common.io import InputReader
from .logic import PageOrderingRule


def parse_page_ordering_rules(input_reader: InputReader) -> Iterator[PageOrderingRule]:
    for line in input_reader.read_stripped_lines():
        if "|" in line:
            before, after = line.split("|")
            yield PageOrderingRule(int(before), int(after))


def parse_updates(input_reader: InputReader) -> Iterator[tuple[int, ...]]:
    for line in input_reader.read_stripped_lines():
        if "|" not in line:
            yield tuple(map(int, line.split(",")))
