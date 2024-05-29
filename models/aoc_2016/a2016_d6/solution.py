from models.common.io import InputReader
from .message_reconstructor import MessageReconstructor


def aoc_2016_d6(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 6: Signals and Noise ---")
    lines = list(input_reader.readlines())
    message_reconstructor = MessageReconstructor(lines)
    most_common_chars = (
        message_reconstructor.reconstruct_message_from_most_common_chars()
    )
    print(
        f"Part 1: Message reconstructed from most common letters: {most_common_chars}"
    )
    least_common_chars = (
        message_reconstructor.reconstruct_message_from_least_common_chars()
    )
    print(
        f"Part 2: Message reconstructed from least common letters: {least_common_chars}"
    )