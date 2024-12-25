from typing import Iterator

from models.common.io import InputReader


def _split_groups(input_reader: InputReader) -> Iterator[list[str]]:
    current_lines = []
    for line in input_reader.read_stripped_lines(keep_empty_lines=True):
        if line:
            current_lines.append(line)
        else:
            yield current_lines
            current_lines = []
    if current_lines:
        yield current_lines


def _parse_heights(lines: list[str]) -> tuple[int, ...]:
    heights = [0] * len(lines[0])
    for line in lines:
        for i, char in enumerate(line):
            if char == "#":
                heights[i] += 1
    return tuple(heights)


def parse_locks(input_reader: InputReader) -> Iterator[tuple[int, ...]]:
    for group in _split_groups(input_reader):
        if set(group[0]) == {"#"}:
            yield _parse_heights(group[1:])


def parse_keys(input_reader: InputReader) -> Iterator[tuple[int, ...]]:
    for group in _split_groups(input_reader):
        if set(group[0]) == {"."}:
            yield _parse_heights(list(reversed(group[:-1])))
