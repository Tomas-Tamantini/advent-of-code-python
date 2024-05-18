from typing import Iterator
from models.common.io import InputReader


def parse_calories(input_reader: InputReader) -> Iterator[tuple[int, ...]]:
    current_calories = []
    for line in input_reader.readlines():
        if line.strip():
            current_calories.append(int(line))
        elif current_calories:
            yield tuple(current_calories)
            current_calories.clear()
    if current_calories:
        yield tuple(current_calories)
