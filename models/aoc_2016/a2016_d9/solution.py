from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .text_decompressor import TextDecompressor


def aoc_2016_d9(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 9, "Explosives in Cyberspace")
    io_handler.output_writer.write_header(problem_id)
    compressed_text = io_handler.input_reader.read().strip()
    decompressor = TextDecompressor(compressed_text)
    result = decompressor.length_shallow_decompression()
    yield ProblemSolution(
        problem_id, f"Length of decompressed text: {result}", result, part=1
    )

    result = decompressor.length_recursive_decompression()
    yield ProblemSolution(
        problem_id, f"Length of recursively decompressed text: {result}", result, part=2
    )
