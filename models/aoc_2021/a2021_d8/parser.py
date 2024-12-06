from typing import Iterator

from models.common.io import InputReader

from .seven_segment_display import ShuffledSevenDigitDisplay


def _parse_shuffled_seven_digit_display(line: str) -> ShuffledSevenDigitDisplay:
    parts = line.split("|")
    unique_patterns = tuple(x.strip() for x in parts[0].split())
    four_digit_output = tuple(x.strip() for x in parts[1].split())
    return ShuffledSevenDigitDisplay(unique_patterns, four_digit_output)


def parse_shuffled_seven_digit_displays(
    input_reader: InputReader,
) -> Iterator[ShuffledSevenDigitDisplay]:
    for line in input_reader.read_stripped_lines():
        yield _parse_shuffled_seven_digit_display(line)
