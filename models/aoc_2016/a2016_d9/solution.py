from models.common.io import IOHandler, Problem
from .text_decompressor import TextDecompressor


def aoc_2016_d9(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 9, "Explosives in Cyberspace")
    io_handler.output_writer.write_header(problem_id)
    compressed_text = io_handler.input_reader.read().strip()
    decompressor = TextDecompressor(compressed_text)
    print(
        f"Part 1: Length of decompressed text: {decompressor.length_shallow_decompression()}"
    )
    print(
        f"Part 2: Length of recursively decompressed text: {decompressor.length_recursive_decompression()}"
    )
