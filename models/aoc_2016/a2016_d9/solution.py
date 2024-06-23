from models.common.io import IOHandler
from .text_decompressor import TextDecompressor


def aoc_2016_d9(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2016 - Day 9: Explosives in Cyberspace ---")
    compressed_text = io_handler.input_reader.read().strip()
    decompressor = TextDecompressor(compressed_text)
    print(
        f"Part 1: Length of decompressed text: {decompressor.length_shallow_decompression()}"
    )
    print(
        f"Part 2: Length of recursively decompressed text: {decompressor.length_recursive_decompression()}"
    )
