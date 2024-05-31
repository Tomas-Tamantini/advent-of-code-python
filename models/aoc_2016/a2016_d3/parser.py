from typing import Iterator
from models.common.io import InputReader


def parse_triangle_sides(
    input_reader: InputReader, read_horizontally: bool
) -> Iterator[tuple[int, int, int]]:

    if read_horizontally:
        for line in input_reader.readlines():
            yield tuple(map(int, line.strip().split()))
    else:
        lines = list(input_reader.readlines())
        for i in range(0, len(lines), 3):
            for j in range(3):
                yield tuple(int(lines[i + k].strip().split()[j]) for k in range(3))
