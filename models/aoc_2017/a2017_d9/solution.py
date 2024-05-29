from models.common.io import InputReader
from .stream_handler import StreamHandler


def aoc_2017_d9(input_reader: InputReader, **_) -> None:
    print("--- AOC 2017 - Day 9: Stream Processing ---")
    stream = input_reader.read().strip()
    handler = StreamHandler(stream)
    print(f"Part 1: Total score: {handler.total_score}")
    print(
        f"Part 2: Number of non-cancelled characters in garbage: {handler.num_non_cancelled_chars_in_garbage}"
    )