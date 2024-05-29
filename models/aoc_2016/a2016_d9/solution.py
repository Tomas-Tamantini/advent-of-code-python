from models.common.io import InputReader
from .text_decompressor import TextDecompressor


def aoc_2016_d9(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 9: Explosives in Cyberspace ---")
    compressed_text = input_reader.read().strip()
    decompressor = TextDecompressor(compressed_text)
    print(
        f"Part 1: Length of decompressed text: {decompressor.length_shallow_decompression()}"
    )
    print(
        f"Part 2: Length of recursively decompressed text: {decompressor.length_recursive_decompression()}"
    )
